# Static Site Generator[^1]
> [!WARNING]
> You need to have python3 installed
## Usage
To use this generator just put some markdown files in the content directory as index.md files.
Then run the main.sh script from the root of the project:
```bash
./main.sh
```
This will start a webserver which you can access in you browser under the url http://localhost:8888.

If you only want to build the html files and not run a server, just run the build.sh script from the root of the project:
```bash
./build.sh
```
The files will be generated in the docs directory.
## Troubleshooting
If something isn't quite working, run the test.sh script from the root of you project:
```bash
./test.sh
```
This should show you more in detail where the Error is.

You can also just submit an issue on my GitHub project page and i will fix that as soon as possible.

[^1]: Made with [boot.dev](https://www.boot.dev)