<p align="center">
  <img src="https://img.icons8.com/?size=512&id=55494&format=png" width="20%" alt="PAINEL-AGROTOXICOS-AGUA-RS-logo">
</p>
<p align="center">
    <h1 align="center">PAINEL-AGROTOXICOS-AGUA-RS</h1>
</p>
<p align="center">
    <em>Engage, Analyze, Act!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/barbara-pietoso/painel-agrotoxicos-agua-rs?style=flat&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/barbara-pietoso/painel-agrotoxicos-agua-rs?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/barbara-pietoso/painel-agrotoxicos-agua-rs?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/barbara-pietoso/painel-agrotoxicos-agua-rs?style=flat&color=0080ff" alt="repo-language-count">
</p>
<p align="center">
		<em>Built with the tools and technologies:</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white" alt="Streamlit">
	<img src="https://img.shields.io/badge/Folium-77B829.svg?style=flat&logo=Folium&logoColor=white" alt="Folium">
	<img src="https://img.shields.io/badge/Plotly-3F4F75.svg?style=flat&logo=Plotly&logoColor=white" alt="Plotly">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">
</p>

<br>

#####  Table of Contents

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
    - [ Prerequisites](#-prerequisites)
    - [ Installation](#-installation)
    - [ Usage](#-usage)
    - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)

---

##  Overview

The painel-agrotoxicos-agua-rs project showcases a web application designed to detect pesticides in water within Rio Grande do Sul. Leveraging libraries like pandas, geopandas, and plotly, the software provides interactive data visualization using map functionalities and components for enhanced visualization. With a user-friendly layout, custom title, and icons, this application offers an engaging user experience for exploring agrochemical contamination in water bodies.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project utilizes a web application architecture built with streamlit, providing an interactive data visualization experience for detecting pesticides in water in Rio Grande do Sul. It leverages libraries like pandas, geopandas, plotly, folium, altair, and streamlit components for enhanced visualization. |
| 🔩 | **Code Quality**  | The codebase demonstrates good code quality and style, employing various libraries efficiently for geospatial data visualization, manipulation, and dashboard creation. The use of modular components enhances readability and maintainability. |
| 📄 | **Documentation** | The project includes detailed documentation within the repository, explaining the purpose, functionality, and usage of the application. The documentation covers essential aspects of the codebase, aiding contributors and users in understanding and extending the project. |
| 🔌 | **Integrations**  | Key integrations include streamlit-echarts, plotly, geopandas, folium, altair, and other libraries for data visualization, mapping, and analysis. External dependencies enhance the application's functionality and provide a rich user experience. |
| 🧩 | **Modularity**    | The codebase exhibits modularity through the use of separate components and libraries for distinct functionalities. This modular design promotes code reusability and facilitates easier maintenance and feature enhancements. |
| 🧪 | **Testing**       | Testing frameworks and tools used in the project are not explicitly mentioned in the provided details. Further investigation may be required to assess the testing strategy and coverage. |
| ⚡️  | **Performance**   | The project's efficiency and speed are enhanced by leveraging optimized libraries for data visualization and manipulation. Resource usage is likely optimized to provide a seamless interactive experience for users exploring pesticide detection data. |
| 🛡️ | **Security**      | Measures for data protection and access control are not explicitly discussed in the provided details. Security considerations may need to be evaluated to ensure data privacy and integrity. |
| 📦 | **Dependencies**  | Key external libraries and dependencies include streamlit-echarts, plotly, geopandas, folium, altair, unidecode, and other essential libraries for geospatial data visualization and manipulation. The requirements.txt file ensures necessary dependencies are installed. |
| 🚀 | **Scalability**   | The project's architecture allows for scalability in handling increased traffic and load as users engage with the interactive data visualization features. The modular design and integration of scalable libraries contribute to the application's ability to accommodate growth. |

---

##  Repository Structure

```sh
└── painel-agrotoxicos-agua-rs/
    ├── app.py
    └── requirements.txt
```

---

##  Modules

<details closed><summary>.</summary>

| File | Summary |
| --- | --- |
| [requirements.txt](https://github.com/barbara-pietoso/painel-agrotoxicos-agua-rs/blob/main/requirements.txt) | Ensures essential libraries for geospatial data visualization and manipulation are available. Facilitates interactive mapping, data analysis, and dashboard creation in the parent repositorys application. |
| [app.py](https://github.com/barbara-pietoso/painel-agrotoxicos-agua-rs/blob/main/app.py) | The app.py file in the painel-agrotoxicos-agua-rs repository houses a comprehensive web application for detecting pesticides in water in Rio Grande do Sul. It leverages various libraries like pandas, geopandas, plotly, and streamlit to provide an interactive data visualization experience. The page is configured with a custom title and icon, offering a wide layout design with a collapsed sidebar for an optimized user interface. The code integrates map functionalities using folium and streamlit-folium, along with additional components for enhanced visualization like altair, unidecode, and streamlit_echarts. This application aims to present data on pesticide detection efficiently and engagingly to users exploring agrochemical contamination in water bodies. |

</details>

---

##  Getting Started

###  Prerequisites

**Python**: `version x.y.z`

###  Installation

Build the project from source:

1. Clone the painel-agrotoxicos-agua-rs repository:
```sh
❯ git clone https://github.com/barbara-pietoso/painel-agrotoxicos-agua-rs
```

2. Navigate to the project directory:
```sh
❯ cd painel-agrotoxicos-agua-rs
```

3. Install the required dependencies:
```sh
❯ pip install -r requirements.txt
```

###  Usage

To run the project, execute the following command:

```sh
❯ python main.py
```

###  Tests

Execute the test suite using the following command:

```sh
❯ pytest
```

---

##  Project Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/barbara-pietoso/painel-agrotoxicos-agua-rs/issues)**: Submit bugs found or log feature requests for the `painel-agrotoxicos-agua-rs` project.
- **[Submit Pull Requests](https://github.com/barbara-pietoso/painel-agrotoxicos-agua-rs/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/barbara-pietoso/painel-agrotoxicos-agua-rs/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/barbara-pietoso/painel-agrotoxicos-agua-rs
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/barbara-pietoso/painel-agrotoxicos-agua-rs/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=barbara-pietoso/painel-agrotoxicos-agua-rs">
   </a>
</p>
</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
