# Code 0: Import dependencies

We import operating system to work with the folders and files.

```python
import os
```

## Code 0.0: Declare function "`filename`" with "`namestring`" as an input.

We define the header: proper filename in relation to current folder is asked, given a "`namestring`" - the filename and extension part of the proper filename.

```python
def filename(namestring):
```

One intent level inside the function, we:
- Ask for current working directory from the operating system functions we imported on the first line.
- Set stepcounter to 0: each time we add 1 to this, we also add one "folder-up" piece ("../") to actual filename reference link we return.

```python
    current_dir = os.getcwd()
    step_count = 0
```

### Code 0.0.0: Recursively search the (configurator) file from the folder tree, from current folder upwards; assuming that configuration files are in the same folder:

We loop until it's broken from inside (main loop of this function):

```
    while True:
```

Going into the loop - one intent level down, we first ask, in beginning of each iteration, whether we can find configurator script, which must be
there even if we have not created a specific configuration file to check, at the current depth.

Inside is the return clause: if it's the first iteration of the loop, step_count is `0`, file already found and the return value equal to the result;
otherwise, each time an iteration has been ran once on this intent level inside "while True:" block, we add one to step_count - if it will be happy
after rounds of iterations, it will be happy to add that many `'../'`'s before actual input string, and thus return the depth factor with actual
relative position of file:

```python
        if os.path.exists(os.path.join(current_dir, "modelselector.py")):
            return '../' * step_count + namestring
```

This is tricky. From `os.path.dirname` we do not get the current directory, but we get *the current directory of the current directory* - by this,
we indeed rather move to parent folder of the current folder to look for our file:

```
        current_dir = os.path.dirname(current_dir)
```

As we moved level up, we add `1` to our level counter: by string multiplication, the actual count is used to repeat '../' as many times as needed,
to make the resulting link point to right place:

```
        step_count += 1
```

At the root level of filesystem, if we still did not find our configuration file and folder, we break the cycle - thus, the second return clause,
which follows with next block, is used instead of the correct return block before:

```python
        if current_dir == os.path.dirname(current_dir):
            break
```

We return the input as-is. While the caller script will throw exception that file is not found, and tell the user that configuration file was not found:
that this string still contains the filename merely means the error message will tell properly, *which* file was not found, satisfying the user's debbuging
needs:

```
    return namestring
```

# Code 1: Test run for the file

We enter this chapter if this script has been ran as an executable python script, not as an import dependency of another script:

```python
if __name__ == "__main__":
```

## Code 1.0: Check for various files, for example (look for proper places of these files):

### Code 1.0a: Check for "`model_select.json`", for example (look for proper place of this file):

Set the "`namestring`" variable: we look for this file:

```python
    namestring = "model_select.json"
```

Use the "`filename`" utility (a function), which was defined before, to look for file "`model_select.json`" stored in variable "`namestring`" by previous line of code:

```python
    result = filename(namestring)
```

Display the result to the user: in case the file is supposed to be in parent folder in case it exists, it would print "`../model_select.json`", but in case we call
this script from parent folder itself - *indeed*, the relative position is "`model_select.json`":

```python
    print(result)
```

### Code 1.0b: Check for "`models_config.json`", for example (look for proper place of this file):

Do the same thing as in previous section, but for another file:

```python
    namestring = "models_config.json"
    result = filename(namestring)
    print(result)  # This will print either "../path/to/example_file.txt" or just "example_file.txt" depending on the location of the script
```
