# BraveFilterSearch
Filter and Search contents of selected Brave Filter Lists. Compare + Add Custom Filters.

![BraveFilterGUI](https://github.com/user-attachments/assets/778b07f9-1fe8-439d-a8e1-926bb1acae1e)

## Overview

**Brave Filter GUI** is a desktop application designed for filtering and searching content from Brave's opt-in list filters. <br>
- Select and search up-to-date Brave opt-in filter lists.
- View your Active and Custom Filters. 
- Compare new filters and Add to custom filters in Brave.

This application is built using Python and the Tkinter library for the graphical user interface. It leverages `pipenv` to manage dependencies. Built for Brave on macOS. 

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
4. **Compare Filters**: Use `Load Custom Filters`. Enter in filters under Add Custom Filters and click `Compare Filters`. (If not selected prior, Active and Custom Filters will be automatically enabled for comparison.) New Filters appear as Green and duplicates appear Red.
   - For more information on Custom Filter Syntax and examples use [this gist](https://gist.github.com/cspence001/a7e50832ba9c682e4b7f53738383b8b9#custom-filters).
5. **Add New Filters**: Clicking `Add New Filters` will add the new filters to Brave Custom Filters. 
   - <b>Important</b>: Ensure Brave Browser App is closed before adding new filters. 

## Example Use-Cases

1. **Identifying Blocked Page Elements**<br>
**Scenario**: You're troubleshooting why a specific image or script isn't loading on a webpage.<br>
**Use**: Input keywords related to the element (like the image URL or script name) into the search box. The tool will display if any filter rules are blocking that element.
2. **Analyzing Website-Specific Filters**<br>
**Scenario**: You want to understand what content is being blocked on a specific website.<br>
**Use**: Enter the website's domain (e.g., example.com) into the search. The results will show which filter rules apply to that site, helping you determine the source of any issues.
3. **Debugging Ad Blockers**<br>
**Scenario**: An ad blocker is interfering with a website's functionality.<br>
**Use**: Search for keywords related to the ads or scripts causing issues. This can help you identify which filters are problematic and allow you to adjust your ad-blocking setup.
4. **Comparing Custom Filters**<br>
**Scenario**: You want to refine your custom filter list by comparing it with active filters.<br>
**Use**: Load your custom filters, compare them with active filters, and see which ones are new (marked in green) or duplicates (marked in red) before adding.

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
