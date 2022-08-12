# Keys

[Sublime Text](https://www.sublimetext.com/) plugin to display mapped keys.

![](keys.png)

## Installation

- Open the command palette with `CMD + SHIT + P`
- Select `Package Control: Add Repository`
- Enter https://github.com/ssanj/OpenTabs for the repository
- Select `Package Control: Install Package`
- Choose Keys


## Functionality

### List all keys

To list all keys press `F1`.

![](key-definitions.gif)

*Note*: If you've defined a filter, they keys will be filtered to show a subset.

### Search by command or key

To search by command name or key(s) use `SHIFT` + `F1`

#### Searching by Command

![Search by command](key-search-command.gif)

#### Searching by Key

![Search by keys](key-search-keys.gif)


## Settings

Sample *Keys.sublime-settings* file:

```
{

  // To filter in *all* packages use:
  // "packages_to_filter_in": ["Packages/"]
  // these names are used as paths so the trailing '/' is required
  "packages_to_filter_in": [
    "Packages/User/",
    "Packages/SymbolView/",
    "Packages/RecentFolders/",
    "Packages/QuickView/",
    "Packages/QuickView/",
    "Packages/OpenWindows/",
    "Packages/OpenTabs/",
    "Packages/OpenSplit/",
    "Packages/Keys/",
    "Packages/Ghomments/",
    "Packages/BlogTools/",
    "Packages/Scoggle/",
    "Packages/Quick File Creator/",
    "Packages/LSP/",
    "Packages/Default/",
  ],

  // If you don't want any mapping use an empty object here
  // "symbol_map": {}
  "symbol_map": {
    "COMMAND": "⌘",
    "SUPER": "⌘",
    "PRIMARY": "⌘",
    "CTRL": "⌃",
    "OPTION": "⌥",
    "ALT": "⌥",
    "SHIFT": "⇧",
    "UP": "↑",
    "DOWN": "↓",
    "TAB": "⇥",
    "LEFT": "←",
    "RIGHT": "→",
  },

  // When debug is true, the settings loaded are written to the logs
  // Also if this setting can't be read (because of some issue with the config)
  // debug is on by default and will write out some useful information.
  "debug": false
}
```

**packages_to_filter_in** - defines the packages to include when doing a search or displaying key definitions. If you want all the packages use a value of `["Packages/"]`. These values are are used as paths so the trailing '/' is required.

**symbol_map** - Mapping between the text in the keymap file and the symbol or alternate text you wish to see. If you don't want any mapping use an empty object here: `{}`

**debug** - Set to `true` if you want to see the settings loaded by Keys. If the settings can't be loaded correctly, this will automatically toggle to true and write out any settings being used as defaults
