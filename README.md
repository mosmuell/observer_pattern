# Observer Pattern

## Overview

The Observer Pattern Package is a Python implementation of the observer design pattern, providing a robust framework for monitoring state changes in objects and notifying registered observers about these changes. This package is particularly useful in scenarios where one object's state is dependent on another's, and changes need to be propagated or reacted to in real-time.

## Features

- **Observable Class**: Central to this package, the `Observable` class allows objects to be monitored for state changes. Instances of this class can notify observers when their properties are modified.

- **Observer Class**: An abstract base class that can be extended to create observers. These observers can register with `Observable` instances to receive notifications about state changes.

- **Change Tracking**: The package offers functionality to track not only the final state change but also the initiation of a change, allowing for more granular control and understanding of the sequence of events.

- **Property and Method Handling**: The package intelligently handles class and instance attributes, including properties and callable methods, ensuring that only relevant changes are notified.

## Installation

```bash
pip install git+https://github.com/mosmuell/observer_pattern
```

## Usage

### Creating an Observable Object

To create an observable object, simply inherit from the `Observable` class:

```python
from observer_pattern import Observable

class MyObservable(Observable):
    def __init__(self, value):
        super().__init__()
        self.value = value
```

### Implementing an Observer

Create an observer by extending the `Observer` class and implementing the `on_change` method:

```python
from observer_pattern import Observer
import logging

logger = logging.getLogger(__name__)


class MyObserver(Observer):
    def __init__(self, observable):
        super().__init__(observable)

    def on_change(self, full_access_path, value):
        logger.info("Observed a change in %s: %s", full_access_path, value)

    def on_change_start(self, full_access_path):
        logger.info("'%s' is being changed", full_access_path)
```

### Registering Observers and Tracking Changes

Observers are automatically registered upon instantiation and are notified of changes:

```python
observable = MyObservable(10)
observer = MyObserver(observable)

observable.value = 20  # Triggers notification to observer
```

## Advanced Topics

### Nested Object Observation

The package supports observing changes in nested objects. If an observable object contains other observable objects, changes in the nested objects are also propagated to the observers.

### Handling Concurrency

In scenarios where multiple attributes are changing concurrently, the package maintains a record of ongoing changes, allowing observers to distinguish between simultaneous updates.

### Customizing Change Notification

Observers can customize their reaction to changes by overriding additional methods provided for start and end of change notifications.

## Contributing

Contributions to the package are welcome. Please follow the standard procedures for contributing to open-source projects on GitHub.

## License

This project is licensed under the [MIT](./LICENSE) license.


## TODOs
- [ ] add observer implementation that watches for changes in property dependencies -> triggers on_change
- [ ] documentation
  - [ ] mention that calling a property getter will also result in an on_change and on_change_start notification
    - [ ] you would have to create a local cache to see if the property value has really changed
