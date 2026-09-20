"""Build a self-contained, compile-checked arXiv source archive.

Only manuscript dependencies are packaged. Experimental records remain in the
public research repository; no credentials, build logs, or rendered paper PDF
are included in the source upload.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'output' / 'submission'
TEX_FILES = [
    'main.tex', 'theory-appendix.tex', 'references.bib',
    'generated/results-macros.tex', 'generated/model-results.tex',
    'generated/receipt-results.tex', 'generated/control-results.tex',
]


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='delegation-arxiv-') as directory:
        source = Path(directory) / 'source'
        build = Path(directory) / 'build'
        source.mkdir()
        build.mkdir()
        for name in TEX_FILES:
            text = (ROOT / 'paper' / name).read_text()
            # Resolve figure paths relative to the original compilation root.
            for figure in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', text):
                original = (ROOT / 'paper' / figure).resolve()
                original.relative_to(ROOT)
                relative = 'figures/' + original.name
                target = source / relative
                target.parent.mkdir(exist_ok=True)
                if target.exists() and target.read_bytes() != original.read_bytes():
                    raise ValueError('Figure basename collision: ' + relative)
                shutil.copy2(original, target)
                text = text.replace('{' + figure + '}', '{' + relative + '}')
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        result = subprocess.run(
            ['tectonic', 'main.tex', '--keep-intermediates', '--keep-logs', '--outdir', str(build)],
            cwd=source, capture_output=True, text=True, check=False,
        )
        (DEST / 'arxiv-local-build.log').write_text(result.stdout + result.stderr)
        result.check_returncode()
        log = (build / 'main.log').read_text(errors='replace')
        for problem in ['Undefined control sequence', 'undefined references', 'undefined citations', 'Overfull \\hbox']:
            if problem in log:
                raise RuntimeError('Manuscript compile issue: ' + problem)
        shutil.copy2(build / 'main.bbl', source / 'main.bbl')
        shutil.copy2(build / 'main.pdf', DEST / 'arxiv-compiled-preview.pdf')
        files = sorted(path for path in source.rglob('*') if path.is_file())
        archive = DEST / 'delegation-blind-spot-arxiv-source.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in files:
                entry = zipfile.ZipInfo(path.relative_to(source).as_posix(), (2026, 9, 20, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o644 << 16
                bundle.writestr(entry, path.read_bytes())
        manifest = {
            'status': 'Prepared, not submitted',
            'top_level_tex': 'main.tex',
            'recommended_arxiv_processor': 'pdflatex',
            'local_validation_processor': 'Tectonic (XeTeX)',
            'note': 'Preview is locally compiled. Inspect arXiv server compilation before submitting.',
            'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
            'files': {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        }
        (DEST / 'arxiv-source-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(f'Prepared {archive.name}: {len(files)} manuscript dependencies, locally compiled.')


if __name__ == '__main__':
    main()
