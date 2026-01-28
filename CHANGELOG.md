# Changelog

All notable changes to ClawdBot Control Panel will be documented in this file.

## [1.0.1](https://github.com/SSujitX/clawdbot-ui/compare/v1.0.1...v1.0.1) (2026-01-28)

### ✨ Features

* add script to automatically generate CHANGELOG.md from git commits. ([d1a3bd1](https://github.com/SSujitX/clawdbot-ui/commit/d1a3bd10152fbc08c2e5459b60ce2d1cf60211de))
* introduce automated CHANGELOG.md generation and version bumping script. ([58467a0](https://github.com/SSujitX/clawdbot-ui/commit/58467a069a799006c575988e39890907397dd7e2))
* auto-create draft release on every push from CHANGELOG.md ([f6454bd](https://github.com/SSujitX/clawdbot-ui/commit/f6454bd64786236bcaf5c1600f706e734580ec89))

### 🐛 Bug Fixes

* **window**: resolve icon path detection in frozen builds ([438e507](https://github.com/SSujitX/clawdbot-ui/commit/438e507e33227c2992a38cce3e3ce5c6d9474eed))
* handle last version in CHANGELOG.md extraction ([9ad3348](https://github.com/SSujitX/clawdbot-ui/commit/9ad33483cea47edc1e8577a09004e1f5d5ba2e55))

### 📝 Documentation

* update CHANGELOG.md for release 1.0.1 ([457d9f0](https://github.com/SSujitX/clawdbot-ui/commit/457d9f06014899a6e272a68b23ecb6b8a9ee5793))
* add build instructions for standalone Windows executable ([f6d80be](https://github.com/SSujitX/clawdbot-ui/commit/f6d80bec00aa9a1f29109335df9c23a080e9e3b0))
* update CHANGELOG.md format and content for release automation ([b30c4ad](https://github.com/SSujitX/clawdbot-ui/commit/b30c4ad79784c98a546cf7359ac7ca988bea1c81))

### ♻️ Code Refactoring

* **release**: simplify changelog generation to single version ([b500ba3](https://github.com/SSujitX/clawdbot-ui/commit/b500ba3dee28f670e7d9e1a1e8d5816ebcac4874))
* **release**: regenerate entire changelog instead of inserting entries ([c9a114e](https://github.com/SSujitX/clawdbot-ui/commit/c9a114e97853ac59aea2abe8204e6f453ade0550))

### 👷 Build System

* improve build script with cleanup and asset inclusion ([c405c3c](https://github.com/SSujitX/clawdbot-ui/commit/c405c3c8543a35f4e1b97d782af1900feddaa0fa))
* add imageio and nuitka dependencies ([baebd28](https://github.com/SSujitX/clawdbot-ui/commit/baebd284855ff629b954e814c11795fbc658a1d7))
* add imageio and nuitka dependencies ([602d8e7](https://github.com/SSujitX/clawdbot-ui/commit/602d8e7a3bfaf89732b7acc08490990ae7b8c5a7))
* add PowerShell script for building executable with Nuitka ([01d86e8](https://github.com/SSujitX/clawdbot-ui/commit/01d86e84790fe5d503018718d7890be63e7597d5))
* revert version and remove commitizen configuration ([1b62481](https://github.com/SSujitX/clawdbot-ui/commit/1b62481e0a4c59820ac21b0c9a3ea1f0317e3177))

### 💚 Continuous Integration

* **release**: update changelog version regex to support flexible version formats ([e8c1e98](https://github.com/SSujitX/clawdbot-ui/commit/e8c1e98a783062fd8554bb089baf806a2994d6ce))
* improve CHANGELOG parsing for release notes ([34fb8df](https://github.com/SSujitX/clawdbot-ui/commit/34fb8df5492d9fb8819be29af0670496f86bd93c))
* **build-windows**: include assets directory in Nuitka build ([015b494](https://github.com/SSujitX/clawdbot-ui/commit/015b4948d1bf1e3e4e5aefd69d048740077e13a1))
* include assets directory in macOS build ([1f02c62](https://github.com/SSujitX/clawdbot-ui/commit/1f02c623e576fcac5dac0c84b6d4dc2d42eb90db))
* add icon to Windows executable build ([cb13c91](https://github.com/SSujitX/clawdbot-ui/commit/cb13c918dc41e1bb5e09fe38a0465b73431df8d9))
* fix GitHub Actions release workflow configuration ([f7d1d5d](https://github.com/SSujitX/clawdbot-ui/commit/f7d1d5d116606df88921a669c399854e4c46fcea))
* simplify draft release name by removing static prefix ([937de51](https://github.com/SSujitX/clawdbot-ui/commit/937de51acfd9cea743099ac4f2f25440f58bad68))

### 🔧 Chores

* remove outdated release workflow documentation ([b4156a8](https://github.com/SSujitX/clawdbot-ui/commit/b4156a88b372d18a94b27e0bff2f784b451565fa))
