# dj-incremental-analysis

- This GitHub action identify **newly** introduced smells in a commit. The supported smells types are `Architecture Smells`, `Design Smells` and `Implementation Smells`.

- A **diff of smells** (i.e., added and removed smells since the last commit) is computed using the [designite_util](https://github.com/tushartushar/designite_util) library. 

- Finally, the action creates *issue(s)* for the identified *diff of smells* automatically.

- Here's an example issue created by this action:

![Example Issue](./docs/images/SampleIssue.png)

## How to use this action?

### Pre-requisites

- **Workflow permission**: Make sure that the `Workflow permissions` of the repository (*settings > Actions > General*) is set to **Read and write permissions**. If it's not the case, the action won't be able to create the issues or download the artifacts.

### Workflow file  
Create a GitHub Action workflow file in the repository. We first needs to analyze the latest commit using DesigniteJava; it can be achieved using `DJAction` action. The `DJAction` action stores the analyzed code quality report in the Actions artifacts. 

The second key step of this exercise is to use this action with the required inputs.
An example of the file is provided below.

```yml
- name: Run Designite analysis for the latest commit
  id: designite
  uses: DesigniteTools/DJAction@v2.0
  with:
    PAT: ${{ secrets.PAT }}

- name: DesigniteJava incremental code quality analysis and issue creation
  uses: DesigniteTools/dj-incremental-analysis@v1.0.0
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    designite-output-old: designite-output-${{ github.event.before }}
    designite-output-new: designite-output-${{ github.sha }}
    repo-name: ${{ github.repository }}             
```

For more details, please checkout this [example repository](https://github.com/IP1102/action-test) using this action. 

