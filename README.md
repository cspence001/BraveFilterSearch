# BraveFilterSearch
Filter and Search contents of selected Brave Filter Lists

![BraveFilterSearchGUI_comp](https://github.com/user-attachments/assets/0098f6bc-6919-40db-8c2b-97f3edafea63)


## Overview

**Brave Filter GUI** is a desktop application designed for filtering and searching content from various filter lists. It allows users to select specific filter lists, search for keywords within the content of these lists, and view the results in an organized manner.

This application is built using Python and the Tkinter library for the graphical user interface. It leverages virtual environments to manage dependencies and ensure a consistent development setup.

---

**Note**: This application utilizes the [latest official catalog](https://github.com/brave/adblock-resources/blob/master/filter_lists/list_catalog.json) of Brave's default and optional adblock lists.
In the browser, the optional lists can be enabled/disabled in settings: `brave://settings/shields/filters`

The following lists are enabled by default:
- **Brave Ad Block Updater**: Default lists for Brave Browser.
- **Brave iOS Specific Filters**: Designed specifically for iOS to address unique adblocking requirements.
- **Brave Ad Block First Party Filters**: Default filters that remain effective in standard blocking mode, regardless of any first-party status.

For more information, see [Brave Blocking Goals & Policy](https://github.com/brave/brave-browser/wiki/Blocking-goals-and-policy)

---
## Installation and Setup

To run this application, you need to have Python and `pipenv` installed on your system. Follow these steps to set up and run the application:

1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone git@github.com:cspence001/BraveFilterSearch.git
   cd BraveFilterSearch
   ```

2. **Install Dependencies**

   Use `pipenv` to install the required dependencies and activate the virtual environment:

   ```bash
   pipenv install
   pipenv shell
   ```

3. **Run the Application**

   Once inside the virtual environment, execute the script to launch the GUI:

   ```bash
   (BraveFilterSearch) bash-3.2$ python3 filter_search_app.py
   ```

4. **Stopping the Application**

   To stop the application, you can close the GUI window or use `Ctrl+C` in the terminal where the script is running.

5. **Create an alias for 1-step launch**

   In your ~/.bash_profile / .zsh / .bash
   ```bash
   alias bravefilterapp="cd ~/path/to/packages/BraveFilterSearch; pipenv run python3 filter_search_app.py"
   ```

### Troubleshooting:

- **Virtual Environment Activation Issue**: If `pipenv shell` does not work or you encounter issues with the virtual environment, you can manually activate it using:

  ```bash
  . .venv/bin/activate
  ```

- **Executable Permission**: If you encounter permission issues when trying to run the script, make sure the script file has executable permissions:

  ```bash
  chmod +x filter_search_app.py
  ```

## Usage

1. **Launching the Application**: After running `filter_search_app.py`, a GUI window will open.
2. **Selecting Filters**: Use the checkboxes on the left to select the filter lists you want to use.
3. **Entering Keywords**: Type a keyword into the search box on the right to filter the content of the selected lists.
4. **Viewing Results**: The search results will be displayed in the main area of the GUI.

## Example Use-Cases

### 1. Identifying Scripts that Block Page Elements

If you're troubleshooting why a specific page element isn't displaying on a webpage, you can use this tool to find out if any filter lists include rules that block that element. 

**Example**: 
- Suppose a page element such as an image or a script is not loading on a website. You can search for keywords related to that element (e.g., the URL or class name) within the filter lists. The results will show if any filter rules are likely to be blocking the element.

### 2. Identifying Filters for Specific Websites

This tool can help you identify which filter rules apply to particular websites. This is useful for understanding what content might be blocked on a website due to specific filter lists.

**Example**:
- If you want to find out which filter rules are applied to `example.com`, you can enter relevant keywords or URL patterns into the search box. The application will display which filter lists contain rules that could affect the content or functionality of `example.com`.

### 3. Debugging Ad Blockers

You can use this tool to debug and refine ad-blocking configurations by analyzing which filters are in place and how they might impact various elements on a website.

**Example**:
- If an ad blocker is causing issues with site functionality, you can review the filter lists and search for keywords related to the problematic ads or scripts. This can help pinpoint which filters are responsible and adjust your ad-blocking setup accordingly.

**Discussions**:
- [How to view what Brave Shields blocks?](https://community.brave.com/t/how-to-view-what-brave-shields-blocks/443285/12) <br>
- [Show which filterlist blocked website](https://community.brave.com/t/adblock-show-which-filterlist-blocked-website/512493)

---
## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your contributions are well-tested and documented.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/cspence001/BraveFilterSearch/blob/main/LICENSE) file for details.

## Contact

For any questions or issues, please [file an issue](https://github.com/cspence001/BraveFilterSearch/issues/new/).
