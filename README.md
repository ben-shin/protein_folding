# protein_folding

Python-based GUI software for processing GFP folding practical data from 96-well CLARIOstar plate reader exports.

This software was made for Imperial College London's Protein Folding Practical, led by Dr. Ernesto Cota.

For help, bug reports, or suggestions, contact Dr. Cota or me at [benwshin@gmail.com](mailto:benwshin@gmail.com).

## What it does

The software can:

* Import one or more CLARIOstar CSV files
* Read wavelength-resolved fluorescence scans
* Organize plate data into a tidy table
* Assign wells and GuHCl concentrations to named practical groups
* Import group assignments from a CSV file
* Export one clean CSV per group
* Plot denaturation curves for any combination of groups
* Fit descriptive and thermodynamic denaturation models
* Plot the full fluorescence spectrum of selected wells or groups
* Customize graph colors, lines, markers, fonts, titles, backgrounds, and legends
* Export graphs, spectra, tidy data, group data, and fit reports

Loading, fitting, and spectrum preparation run in the background so the GUI remains responsive on slower computers.

## Importing plate-reader data

The importer accepts several common CSV layouts:

1. CLARIOstar wavelength-scan exports
2. Long tables containing a `Well`, `Well ID`, `Position`, or similar column
3. An 8 × 12 plate grid with rows A–H
4. A simple well-versus-value table

Imported data are converted into a tidy table containing:

```text
plate_id
source_file
well
row
column
measurement
wavelength_nm
excitation_nm
value
```

The wavelength and excitation columns are included when they are present in the source file.

If a file contains several numerical readouts, they can be selected through the **Signal** menu.

## Assigning practical groups

Wells can be selected manually using the interactive 96-well plate map.

The consecutive-well helper can also select a chosen number of wells in:

* Row-major order
* Column-major order

Each practical group stores:

```text
Group name
Plate identity
Measurement signal
Analysis wavelength
Ordered wells
Ordered GuHCl concentrations
```

The number of conditions is not hardcoded. Groups can contain any number of conditions, although at least eight observations are recommended for the two-state thermodynamic fit.

## Group-map CSV files

A group-map CSV can automatically assign groups after the plate files have been loaded.

The required columns are:

```csv
group name,plate number,well ranges
A1,P1,A1-B4
A2,P1,B5-C8
```

The plate number must match the plate-reader filename without `.csv`.

For example:

```text
Plate file: P1.csv
Plate number in group map: P1
```

Well ranges are expanded in plate order. For example:

```text
A1-B4
```

means:

```text
A1, A2, A3, ..., A12, B1, B2, B3, B4
```

You can also include a concentration column:

```csv
group name,plate number,well ranges,concentrations
A1,P1,A1-B4,"0,0.4,0.8,1.2,1.6,2.0,2.4,2.8,3.2,3.6,4.0,4.4,4.8,5.2,5.6,6.0"
```

If every imported group contains the same number of wells and the concentration column is missing, the software will ask for the GuHCl concentration order once and apply it to every group.

If the groups contain different numbers of wells, concentrations must be included in the group-map CSV.

Examples are available in the `examples` folder.

## Exporting group data

Each practical group is exported as:

```text
<group_name>.csv
```

with these columns:

```text
GuHCl concentration (M)
raw fluorescence values
normalized fluorescence values
```

Normalization uses min-max scaling within each group:

```text
(value - minimum)/(maximum - minimum)
```

The full tidy dataset and the group-assignment mapping can also be saved.

## Denaturation analysis

The analysis panel can display one, several, or all practical groups on the same graph.

Available models are:

1. Four-parameter logistic
2. Two-state linear extrapolation model
3. Auto compare
4. Fit both

### Four-parameter logistic model

The four-parameter logistic model provides a descriptive sigmoidal fit and transition midpoint.

It does not independently provide a thermodynamic folding free energy.

### Two-state thermodynamic model

The thermodynamic model uses:

```text
ΔG_unfold([D]) = ΔG°unfold,H2O - m[D]
Cm = ΔG°unfold,H2O / m
```

It reports:

* ΔG°unfold,H2O in kJ/mol
* ΔG°fold,H2O = −ΔG°unfold,H2O
* m-value in kJ/mol/M
* Cm in M GuHCl
* Covariance-derived standard errors
* RMSE
* R²
* AIC
* AICc
* BIC

The fit-summary table can be sorted by clicking any column header. Clicking the same header again reverses the order.

## Scientific interpretation

A logistic curve alone does not provide a thermodynamic folding free energy.

Free-energy values are only reported by the two-state linear extrapolation model. The directly fitted value is the unfolding free energy in water:

```text
ΔG°unfold,H2O
```

The corresponding folding free energy is:

```text
ΔG°fold,H2O = −ΔG°unfold,H2O
```

These values should only be interpreted when the experiment is close to equilibrium and GFP behaves approximately as a reversible two-state system under the experimental conditions.

## Well spectra

The spectra panel can plot fluorescence intensity against emission wavelength for:

* Individual wells
* Several selected wells
* Every well in a practical group
* Every available well in a plate

Spectra can be displayed as:

* Raw fluorescence
* Peak-normalized fluorescence

The plotted spectrum data can also be exported as CSV.

## Plot customization

Denaturation and spectrum plots can be customized without rerunning the fit.

Available controls include:

* Color palette
* Individual series colors
* Line style
* Line width
* Marker shape
* Marker size
* Opacity
* Plot background
* Grid visibility
* Font family
* Font size
* Plot title
* Axis labels
* Legend visibility
* Legend position

Legend positions include automatic placement, positions inside the graph, outside-right placement, and placement below the graph.

Graphs can be saved as PNG, PDF, or SVG.

## Current limitation

All wells belonging to one practical group must currently come from the same plate-reader CSV file.

A group cannot yet combine conditions across several plates.

## Portable application

Portable builds include Python and all required libraries. The user does not need to install Python or Conda.

Separate builds are required for:

* Windows x64
* Linux x64
* macOS Apple Silicon
* macOS Intel

Download the correct archive from the repository's **Releases** or **Actions** page, extract the full folder, and launch:

```text
Windows: ProteinFoldingPractical.exe
Linux: ProteinFoldingPractical
macOS: ProteinFoldingPractical.app
```

Keep the full extracted folder together. Do not move only the executable out of it.

## Installation from source

Python 3.9 or newer is supported.

### Windows PowerShell

```powershell
git clone https://github.com/ben-shin/Protein-Folding-Practical.git
cd Protein-Folding-Practical

conda env create -f .\environment.yml
conda activate proteinfoldingpractical
python -m pip install -e . --no-deps

.\launch_windows.ps1
```

### Linux

```bash
git clone https://github.com/ben-shin/Protein-Folding-Practical.git
cd Protein-Folding-Practical

conda env create -f environment.yml
conda activate proteinfoldingpractical
python -m pip install -e . --no-deps

chmod +x launch_linux.sh
./launch_linux.sh
```

### macOS

```bash
git clone https://github.com/ben-shin/Protein-Folding-Practical.git
cd Protein-Folding-Practical

conda env create -f environment.yml
conda activate proteinfoldingpractical
python -m pip install -e . --no-deps

chmod +x launch_macos.command
./launch_macos.command
```

After the initial setup, the launcher automatically loads the correct Conda environment and starts the application.

## Practical workflow

1. Export the CLARIOstar measurements as CSV files.
2. Open the application.
3. Load one or more plate CSV files.
4. Select the plate, measurement signal, and analysis wavelength.
5. Assign wells manually or load a group-map CSV.
6. Confirm the GuHCl concentration order.
7. Export the practical-group CSV files.
8. Open the denaturation-analysis tab.
9. Select one or more groups.
10. Choose a fitting model and run the analysis.
11. Check the fitted curve, parameter uncertainties, and fit-quality statistics.
12. Customize and export the graph.
13. Use the well-spectra tab to inspect individual wells or complete groups.

## Running the tests

```bash
python -m pytest -q
```

## Building portable applications

Portable builds are created using GitHub Actions because Windows, Linux, and macOS applications must be built on their respective operating systems.

Open the repository's **Actions** page and run:

```text
Build portable apps
```

To create a release automatically:

```bash
git tag v0.4.1
git push origin v0.4.1
```

The workflow builds and tests the application for each supported platform and attaches the completed archives to the GitHub release.

---

Designed by [Ben Shin](http://ben-shin.github.io/)
