# Changelog

All notable changes to the **Gaming Statistics Dashboard** project will be documented in this file.

The entries are organized by development milestones. Version labels in the historical Sprint entries do not imply that a release tag has been published.

---

## [Unreleased] — Final review, 2026-10-13

Prepared for the owner's final commit; this entry does not claim a published release or successful remote deployment.

### Added

- Shared configuration for project-relative database paths and independent refresh intervals.
- Developer information in Details, loaded on demand and cached.
- Parallel RAWG import ranges with independent HTTP sessions, a bounded queue and a single SQLite writer.
- Rating standard deviation in the Statistics metrics.
- RAWG and Steam attribution links on every page through the sidebar.
- Final QA report and tests covering cache, request counts, transactions, paths and import workflows.

### Changed

- RAWG Home refreshes after 24 hours; Steam refreshes after 15 minutes, checked on reruns.
- Home loads only its displayed 50 records with SQL LIMIT.
- Statistics reuse one prepared DataFrame.
- RAWG authentication, transport and JSON errors share one implementation.
- Runtime and development requirements are separate; CI compiles src/tests and runs the offline test suite.
- Maintained import scripts are included in Git; the local historical CLI is excluded from the delivered suite.
- README, project pitch, plan and final report describe implemented behavior rather than unverified future outcomes.

### Fixed

- Old game cards remain visible if loading the next API page fails or returns no games.
- RAWG rating=0 is exposed as missing/N/A, including older snapshots.
- Malformed records and non-finite numeric values no longer crash normalization.
- SQLite connections close after commit/rollback.
- App and scripts resolve relative database overrides against the project, including configuration loaded from .env.
- Statistics imports work in package and Streamlit script modes.

### Verification

See [Final QA](FINAL_QA.md) for commands, results and limitations. Previous Sprint entries below are historical development records, not Git release-tag evidence.

---

## [v0.3.0] - Sprint 3: Data Analysis, Visualization & Advanced Features

**Period:** 25–29 September 2026  
**Status:** Completed

Sprint 3 focused on extending the Gaming Statistics Dashboard from a data presentation system into a system that can also process, analyze, visualize, filter, sort, and compare game data.

### Added

- Added Data Cleaning and Data Preparation workflow for game data.
- Added data normalization for RAWG game data.
- Added handling for numeric, date, genre, platform, and optional game fields.
- Added Exploratory Data Analysis (EDA) for game data.
- Added descriptive statistical analysis for relevant game attributes.
- Added summary statistics including count, mean, median, minimum, maximum, and standard deviation where applicable.
- Added genre frequency and proportion analysis.
- Added platform frequency and proportion analysis.
- Added average rating analysis by genre.
- Added release-year distribution analysis.
- Added Metacritic score analysis.
- Added Steam live player analysis.
- Added Statistics Dashboard page.
- Added Data Visualization for game statistics.
- Added Genre Distribution visualization.
- Added Platform Distribution visualization.
- Added Rating by Genre visualization.
- Added Release Year Distribution visualization.
- Added Metacritic Score Distribution visualization.
- Added Top Live Steam Players visualization.
- Added Advanced Filtering for Genre, Platform, Minimum Rating, and Release Year.
- Added Advanced Sorting for Rating, Release Date, and Game Name.
- Added ascending and descending sorting options.
- Added Game Comparison functionality.
- Added comparison of supported game attributes such as Rating, Metacritic Score, and Steam Players.
- Added empty-state handling for cases where no data matches the selected filters.
- Added Sprint 3 statistical analysis test cases.
- Added Sprint 3 data processing test cases.
- Added Sprint 3 visualization and integration test coverage.
- Added Sprint 3 daily task allocation and actual work results.

### Changed

- Updated the application workflow to include Data Processing and Analysis before displaying statistical results.
- Updated the Dashboard workflow to support Statistics and Data Visualization.
- Updated data processing to prepare RAWG and Steam data for analysis.
- Updated game filtering to support additional filtering conditions.
- Updated game sorting to support multiple fields and sorting directions.
- Updated the Dashboard to support game comparison.
- Updated the project structure by adding analysis-related components.
- Updated the documentation to reflect Sprint 3 implementation and completed features.
- Updated the project roadmap and Sprint documentation after Sprint 3 completion.

### Fixed

- Improved handling of missing or incomplete game data during analysis.
- Improved handling of non-numeric values before performing statistical calculations.
- Improved consistency of processed data used by the Dashboard.
- Improved handling of empty datasets after applying filters.
- Improved handling of missing values during sorting and comparison.
- Fixed data processing issues that could affect statistical calculations and visualization.
- Fixed integration issues between processed data, analysis functions, and Dashboard components.

### Testing

Sprint 3 testing covered:

- Data Processing
- Data Cleaning
- Data Normalization
- Statistical Analysis
- Dashboard Statistics
- Data Visualization
- Advanced Filtering
- Advanced Sorting
- Game Comparison
- Empty-State Handling
- Dashboard Integration
- Regression Testing

---

## Planner / Coder / Debugger Roles — Sprint 3

| สมาชิก | ชื่อเล่น | Role | หน้าที่ |
|---|---|---|---|
| นายเดโชชิต โตวินัส | ออม | Planner | Defined Sprint 3 scope, requirements, task allocation, Definition of Done, progress tracking, and Sprint 3 documentation. |
| นายชิษณุพงศ์ ซู | คิม | Coder | Developed data preparation, data processing, analysis, statistics, visualization, filtering, sorting, comparison, and integration features. |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Debugger | Tested data quality, statistical outputs, visualization, filtering, sorting, comparison, integration, edge cases, and verified fixes. |

---

## [v0.2.0] - Sprint 2: Web Application, API & Database

**Period:** 20–24 September 2026  
**Status:** Completed

Sprint 2 transformed the project from a CLI Application into a Web Application and introduced external APIs and database storage.

### Added

- Added Streamlit Web Application.
- Added Web Dashboard with navigation.
- Added RAWG API integration for real game data.
- Added RAWG game search and pagination.
- Added Steam API integration.
- Added Steam current player count.
- Added Steam Top 100 / Live Players feature.
- Added SQLite database for game data storage.
- Added Game Service for application logic.
- Added data processing and data normalization.
- Added Game Library.
- Added Genre, Platform, and Rating filters.
- Added Top Rated Games page.
- Added Game Detail page.
- Added pagination for game data.
- Added API and database error handling.
- Added empty-state handling for unavailable data.
- Added Steam player data refresh and snapshot system.
- Added automated tests for API, database, service, and data processing modules.
- Added Sprint 2 daily task allocation and contribution metrics.

### Changed

- Changed the application from CLI to Web Application.
- Changed game data source from local sample data to RAWG API.
- Changed data management from local data to SQLite database.
- Updated project structure by separating API, database, service, data processing, and UI components.
- Updated game search and data retrieval workflow.
- Updated error handling for API and database operations.

### Fixed

- Fixed handling of API errors and unavailable data.
- Fixed data format inconsistencies from API responses.
- Fixed handling of missing game information.
- Fixed large game data display by adding pagination.

## Planner / Coder / Debugger Roles — Sprint 2

| สมาชิก | ชื่อเล่น | Role | หน้าที่ |
|---|---|---|---|
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Planner | Defined Sprint 2 scope, requirements, Web Application plan, system architecture, task allocation, and Sprint 2 documentation. |
| นายเดโชชิต โตวินัส | ออม | Coder | Developed the Streamlit Web Application, RAWG API, Steam API, SQLite database, Game Service, data processing, and application features. |
| นายชิษณุพงศ์ ซู | คิม | Debugger / QA | Tested Web Application, APIs, database, data processing, error handling, edge cases, and verified Sprint 2 features. |

---

## [v0.1.0] - Sprint 1: CLI Foundation

**Status:** Completed

Sprint 1 established the initial application foundation using a Command Line Interface (CLI) and a local sample dataset.

### Added

- Created Gaming Statistics Dashboard project.
- Added project structure and documentation files.
- Added CLI application with main menu and navigation.
- Added local sample game dataset.
- Added game search functionality.
- Added game statistics functionality.
- Added genre and top-rated game views.
- Added input validation and error handling.
- Added Sprint 1 testing and QA test cases.
- Added Sprint 1 daily task allocation and contribution metrics.

### Changed

- Updated project documentation based on Sprint 1 requirements.
- Updated project plan and Sprint 1 documentation.
- Updated Learning Log and Change Log for Sprint 1.

## Planner / Coder / Debugger Roles — Sprint 1

| สมาชิก | ชื่อเล่น | Role | หน้าที่ |
|---|---|---|---|
| นายชิษณุพงศ์ ซู | คิม | Planner | Defined the project scope, requirements, Sprint 1 plan, documentation, and daily task allocation. |
| นายภานุวัฒน์ ผองแก้ว | ฟลุ๊ค | Coder | Developed the CLI application, main menu, game search, statistics, genres, top-rated games, and input validation. |
| นายเดโชชิต โตวินัส | ออม | Debugger / QA | Tested system functions, checked invalid inputs and edge cases, and verified the results of Sprint 1 features. |