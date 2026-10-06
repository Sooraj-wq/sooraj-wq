# A repository-hosted contribution graph

This version removes both third-party graph services. GitHub Actions fetches your contribution calendar from GitHub and saves a mint heatmap as assets/contributions.svg. The README displays that saved file. If a refresh fails, the last successful graph stays visible.

## Install

1. Extract the ZIP and upload README.md, assets/, scripts/, and .github/ into the root of Sooraj-wq/sooraj-wq on main. Include the hidden .github folder (Ctrl+H shows hidden files on Linux). Keep all folder paths intact. Do not upload the ZIP itself.
2. Open the repository’s Actions tab. Enable Actions if prompted.
3. Select Refresh contribution graph → Run workflow → Run workflow. Uploading the workflow and script to main should also start it automatically.
4. Wait for the run to finish successfully, then refresh your profile. Until that first success, the included image shows an honest setup message, not sample contributions.

The workflow requests contents: write to commit only assets/contributions.svg. It uses GitHub’s automatic repository token; no personal access token or external service is required. It is configured to refresh daily at 07:53 India time, though GitHub may delay scheduled runs. Graph data reflects the contribution calendar visible to this token, rather than a raw commit log.

If the run fails, open its failed step to see the error. Repository policies or branch protection may prevent the bot from committing; this has not been tested in your GitHub account. The generator was locally checked with test data, including an empty-activity year. API errors do not overwrite an existing graph.

GitHub can disable scheduled runs after prolonged repository inactivity; manually run or re-enable the workflow in Actions if needed.
