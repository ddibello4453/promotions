# Promotions Service

[![Build Status](https://github.com/CSCI-GA-2820-SP24-001/promotions/actions/workflows/tdd-tests.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-001/promotions/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP24-001/promotions/graph/badge.svg?token=Z88A09R325)](https://codecov.io/gh/CSCI-GA-2820-SP24-001/promotions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

```
Endpoint                         Methods       Rule
-------------------------------  ------------  ------------------------------
create_promotions                POST          /promotions
delete_promotions                 DELETE        /promotions/<int:promotion_id>
get_product                      GET           /promotions/<int:promotion_id>
index                            GET           /
list_promotions                  GET           /promotions
static                           GET           /static/<path:filename>
update_promotions                PUT           /promotions/<int:promotion_id>
```

Test Coverage 97% test coverage and can be run with `make test`

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
