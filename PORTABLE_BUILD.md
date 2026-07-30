# Portable build notes

The portable packages bundle the application and all Python dependencies. Users only unzip the package and launch it.

## Output

- Windows: `dist/ProteinFoldingPractical/ProteinFoldingPractical.exe`
- Linux: `dist/ProteinFoldingPractical/ProteinFoldingPractical`
- macOS: `dist/ProteinFoldingPractical.app`

The package uses PyInstaller one-folder mode for faster startup. The executable depends on the bundled `_internal` directory, so distribute the entire folder or app bundle.

## Automated builds

Run `.github/workflows/build-portable.yml` from GitHub Actions. It builds and tests four artifacts:

1. Windows x64
2. Linux x64
3. macOS Apple Silicon
4. macOS Intel

PyInstaller is not a cross-compiler. Each artifact is built on its target operating system.

## Signing

The workflow creates unsigned builds. Signing and macOS notarization require private certificates and account credentials that are not included in the repository.
