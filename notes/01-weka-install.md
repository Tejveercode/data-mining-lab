# 01 — Experiment 1: Download and install Weka

> **Aim.** To download Weka from the official website and install it on the system, and to verify that the installation works.
>
> **Course outcomes.** CO1 (data mining process and preparing data for processing).
>
> **Time.** 15 minutes if Java is already present, 40 if it is not.

## 1. What Weka is (the viva answer)

Weka — **Waikato Environment for Knowledge Analysis** — is a free, open-source collection of machine-learning algorithms written in Java, developed at the University of Waikato, New Zealand. It is distributed under the GNU GPL. Its value in a teaching lab is that every algorithm is available through a GUI, so you can see the algorithm's parameters and output without writing code, and the same algorithms can be called from the command line or from your own Java program.

It is *not* a database and it is *not* a programming language. It reads a dataset, runs an algorithm on it, and shows you the model and its evaluation.

**Why Java matters:** Weka is a `.jar` file. Without a Java runtime, double-clicking it does nothing at all — no error window, no message. That single fact explains most failed installations.

## 2. The four applications you will be asked to name

When Weka starts, the **GUI Chooser** appears. It offers:

| Application | What it is for | Used in |
|---|---|---|
| **Explorer** | the main workbench: load data, preprocess, classify, cluster, associate, select attributes, visualise | Experiments 2, 4, 6 (and most of the course) |
| **Experimenter** | runs many algorithms over many datasets and compares them statistically | research; not needed here |
| **KnowledgeFlow** | drag-and-drop pipeline builder for the same algorithms | optional |
| **Workbench** | all of the above in a single window with multiple tabs | when you want everything at once |
| **Simple CLI** | a command prompt for Weka commands | Experiment 2, step 2 in your notebook |

## 3. Download (official source only)

1. Open a browser and go to the official page: **https://www.cs.waikato.ac.nz/ml/weka/downloading.html**
2. Choose the right build:
   - **3.8.x** — the stable release. Use this in a lab.
   - **3.9.x** — the development release, newer algorithms, occasionally rough.
3. Choose the right file for the operating system:

| OS | File to take | Note |
|---|---|---|
| Windows | `weka-3-8-x-azul-zulu-windows.exe` (64-bit) | the `zulu` build **bundles Java**, so it just works |
| Windows (no bundled Java) | `weka-3-8-x-oracle-jvm.exe` | needs Java 8+ already installed |
| macOS | `weka-3-8-x-azul-zulu-macos-aarch64.dmg` (Apple silicon) or `...-x64.dmg` (Intel) | drag to Applications |
| Linux | `weka-3-8-x.zip` or `weka-3-8-x.tar.gz` | portable, just unzip |

The file is roughly 60–90 MB. If the download page offers a `.exe` for Windows, prefer the one containing `zulu`: the alternative fails silently when Java is absent.

## 4. Install

### Windows

1. Locate the downloaded `.exe` in `Downloads`.
2. Double-click it. If Windows shows a blue "Windows protected your PC" box, click **More info → Run anyway** (the installer is unsigned, not dangerous).
3. Accept the licence, keep the **default installation path**, keep the default Start-menu folder, click **Next → Install → Finish**.
4. Launch it from the **Start menu** by typing `Weka`.

### macOS

1. Open the downloaded `.dmg`.
2. Drag the Weka icon into **Applications**.
3. Launch from Applications (or Spotlight: `⌘ + Space`, type `weka`).
4. First launch only: right-click the icon → **Open**, then **Open** again, to get past Gatekeeper.

### Linux

```bash
tar -xzf weka-3-8-6.tar.gz          # or: unzip weka-3-8-6.zip
cd weka-3-8-6
java -jar weka.jar                  # starts the GUI Chooser
```

If `java -jar` complains, install a runtime first: `sudo apt install default-jre` (Debian/Ubuntu) or `sudo dnf install java-11-openjdk` (Fedora).

Run it from a terminal every time with a one-line script so you never have to remember the path:

```bash
echo 'alias weka="java -jar ~/weka-3-8-6/weka.jar"' >> ~/.bashrc
```

## 5. Verify the installation (the step that earns the mark)

A successful install shows **all** of the following:

1. The **Weka GUI Chooser** window opens, with the four application buttons and the version number in the title bar.
2. Clicking **Explorer** opens the workbench with six tabs across the top: **Preprocess, Classify, Cluster, Associate, Select attributes, Visualize**.
3. In **Preprocess**, the **Open file…** dialog opens and shows a `data` folder — the sample datasets ship with Weka. `iris.arff` and `weather.nominal.arff` are in it.
4. Under **Tools → Simple CLI** (or the Simple CLI button), typing this prints a summary of the iris dataset with 150 instances and 5 attributes:

```
java weka.core.Instances data/iris.arff
```

If the GUI opens but the `data` folder is empty, you unzipped into the wrong directory — the `data` folder sits next to `weka.jar`, not inside it.

## 6. The five failures that actually happen, and their fixes

| Symptom | Cause | Fix |
|---|---|---|
| Double-click does nothing | no Java, or a 32-bit build on a 64-bit OS | install a JRE; use the `zulu` build |
| `Error: could not open ... weka.jar` | wrong working directory | `cd` into the Weka folder first |
| GUI opens but is blank / fonts are boxes | old Java or a broken font cache | install Java 11+ |
| `Unable to access jarfile` | the path contains spaces and was not quoted | quote the path: `java -jar "C:/Program Files/Weka/weka.jar"` |
| Datasets missing in Open dialog | extracted only the jar, not the whole archive | extract the full archive |

## 7. Write this on paper

> **Aim.** To download and install Weka on the system and verify the installation.
>
> **Theory.** Weka (Waikato Environment for Knowledge Analysis) is an open-source machine-learning toolkit written in Java and developed at the University of Waikato, New Zealand. It provides a collection of data pre-processing, classification, clustering, association-rule and visualisation tools through a graphical interface (Explorer), a command line (Simple CLI) and a Java API. Because it is written in Java it is platform independent, and it requires a Java runtime environment to execute. Datasets are supplied in ARFF (Attribute-Relation File Format), a text format with three sections: relation declaration, attribute declarations and data.
>
> **Procedure.**
> 1. Open the browser and visit the official Weka download page.
> 2. Select the stable release (3.8.x) and the package matching the operating system.
> 3. Download the installer and run it.
> 4. Accept the licence and continue with the default installation directory.
> 5. Complete the installation and launch Weka from the Start menu (or by `java -jar weka.jar` on Linux/macOS).
> 6. Verify that the GUI Chooser appears with Explorer, Experimenter, KnowledgeFlow, Workbench and Simple CLI.
> 7. Open Explorer and confirm that the six tabs and the bundled `data` folder are present.
>
> **Result.** Weka was installed successfully and the Explorer loaded the bundled iris dataset (150 instances, 5 attributes), confirming a working installation.

## 8. Viva questions for Experiment 1

**Q: In one line, what is Weka?**
A free, open-source Java toolkit of machine-learning algorithms with a GUI, a CLI and an API, from the University of Waikato.

**Q: Why is Weka called platform independent?**
Because it runs on the Java Virtual Machine: the same `weka.jar` runs on Windows, macOS and Linux wherever a JRE exists.

**Q: What is ARFF?**
Attribute-Relation File Format — Weka's plain-text data format, in three sections: `@relation`, `@attribute` (one line per column, with its type or nominal values), and `@data` (one row per instance). `%` starts a comment and `?` marks a missing value.

**Q: What are the four applications in the GUI Chooser?**
Explorer, Experimenter, KnowledgeFlow, Workbench (plus Simple CLI).

**Q: Which tab would you use to find outliers?**
Preprocess — it shows per-attribute statistics including min, max, mean, standard deviation and the number of missing values; the Visualize tab shows them as plots.

**Q: Is Weka free for commercial use?**
Yes, it is released under the GNU General Public License.

**Q: What is the difference between Weka 3.8 and 3.9?**
3.8.x is the stable branch; 3.9.x is the development branch with newer algorithms and occasional instability.

**Q: Why did your notebook install the "zulu" build?**
Because it bundles a Java runtime, so installation cannot fail for lack of Java.

**Q: Can Weka read CSV?**
Yes, through Preprocess → Open file (choose CSV in the file-type list) or the `CSVLoader` converter; the file must be converted to ARFF internally, and the first row is treated as attribute names.
