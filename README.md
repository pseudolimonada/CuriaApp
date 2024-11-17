# pgi2024

## Github Organization:

The branch organization is as follows:
![alt text](image.png)

There is a backend branch and a frontend branch, called "end branches".

With feature branches in each (try to keep a feature branch open for no later than a week). Whenever a feature branch gets merged into the respective end branch, the other end must be rebased to account for the changes.

i.e I implement a backend-feature-1 and merge into backend. Then, i rebase frontend into backend.

There is also a main branch. Once one of the end branches has a working prototype, it can perform a pull request to the main branch.

## venv installation

Install the venv

```sh

python -m venv ./.venv
```

Source it (can be automated, google it 😬)

On unix based systems

```.sh
source .venv/bin/activate
```

On windows

```powershell
 .venv\Scripts\activate
```


