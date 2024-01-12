# designite-diff-action
Reusable GitHub Action with (upcoming) support for GitLab.

## What does this action do?

- This action is used to generate and identify **newly** introduced smells in a commit. As of now, it only supports `Architecture Smells`, `Design Smells` and `Implementation Smells`.

- The diff is calculated using the [designite_util](https://github.com/tushartushar/designite_util) library. More information on how it identifies the diff between generated output csv can be found in the repository's README.

- Finally, based on the identified new smells, the action creates *issue(s)* for the same automatically.

- Here's an exaple issue created by this action:

![Example Issue](docs\images\SampleIssue.png)

## How to use this action?

Using this action is pretty straightforward. But there are a few pre-requisites that are needed to be followed.

- **Workflow Permission**: Make dure the `Workflow Permissions` of the repository (*settings > Actions > General*) is set to **Read and write permissions**. If it's not the case, `GITHUB_TOKEN` used in this action, won't be able to create the issues or download the artifacts.

- Have [DesigniteJava jar](https://www.designite-tools.com/designitejava/) in your repository.
  
- Finally, there must be 3 stages in your workflow file:  
    - **Stage 1:** Run DesigniteJava jar on the current commit.
    - **Stage 2:** Upload the output of the `jar` file run as artifacts. Please note that these artifacts expire after <u>**90 days**</u>. 
    - **Stage 3:** Use this action. It will download the artifact from the previous commit (if exists), find the diff with the present commit and if there exists new smells, it'll create issues forthe same.

An example of the 3 stages from a workflow file is as follows:

```yml
- name: Run Designite
id: designite
run: |
    java --version
    echo "${{env.DESIGNITE_OUTPUT}}"
    java -jar ./.github/DesigniteJava.jar -i ./ -o "${{env.DESIGNITE_OUTPUT}}" -d

- name: Archive Designite results
uses: actions/upload-artifact@v3
with:
    name: designite-output-${{ github.sha }}
    path: "${{env.DESIGNITE_OUTPUT}}"

- name: Designite diff action
uses: IP1102/designite-diff-action@v1.0.0-alpha
with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    designite-output-old: designite-output-${{ github.event.before }}
    designite-output-new: designite-output-${{ github.sha }}
    repo-name: ${{ github.repository }}             
```

For more details, please checkout this [example repository](https://github.com/IP1102/action-test) using this action. 

