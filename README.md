# Static Site Generator[^1]
> [!WARNING]
> You need to have python3 installed for this project to work.
## Usage
To use this generator, put some markdown files in the content directory as index.md files. If you want to add content that isn't html, put it into the static directory and it will be copied into the docs directory.

Then run the main.sh script from the root of the project:
```bash
./main.sh
```
The files will be saved inside of the docs directory.
Use the --server flag to start a webserver which you can access in you browser under the url http://localhost:8888:
```bash
./main.sh --server
```
## Troubleshooting
If something isn't quite working, run the test.sh script from the root of you project:
```bash
./test.sh
```
This should show you more in detail where the Error is.

You can also just submit an issue on my GitHub project page and i will fix that as soon as possible.

[^1]: Made with [boot.dev](https://www.boot.dev)