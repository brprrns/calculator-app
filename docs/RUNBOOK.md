# Runbook: Calculator CI/CD (GitHub -> Jenkins -> Docker -> AWS)

## 1. Architecture

```
 Developer
    |  git push (main)
    v
 +--------+   webhook (HTTPS)   +--------+   tunnel   +---------------------------+
 | GitHub | ------------------> | ngrok  | ---------> | Jenkins (Windows machine) |
 +--------+                     +--------+            +-------------+-------------+
                                                                    |
                                          runs the pipeline inside a Docker container
                                                                    v
                                      +---------------------------------------------+
                                      |  Docker agent (python:3.12 + pytest + SAM)  |
                                      |  1. pytest        (CI)                      |
                                      |  2. python -m build -> wheel/sdist  (CI)    |
                                      |  3. sam build                       (CI)    |
                                      |  4. sam deploy                      (CD)    |
                                      +----------------------+----------------------+
                                                             | AWS credentials from Jenkins
                                                             v
                                   +---------------- AWS (ap-south-1) ----------------+
                                   |  CloudFormation stack "calculator-stack"         |
                                   |    - API Gateway  /calculate (GET, POST)         |
                                   |    - Lambda function (Python 3.12)               |
                                   |    - IAM execution role, S3 bucket for artifacts |
                                   +--------------------------------------------------+
```

## 2. One-time setup

### 2.1 Docker Desktop (Windows)
1. Install Docker Desktop (it will ask to enable WSL 2, say yes and reboot if asked).
2. Start it. Make sure it is in **Linux containers** mode (right-click the whale icon; if it says "Switch to Windows containers" you are already on Linux).
3. Check in PowerShell:
   ```
   docker version
   docker run --rm hello-world
   ```

### 2.2 Let Jenkins use Docker
Jenkins installed with choco runs as a Windows service under the SYSTEM account, and that account usually cannot talk to Docker Desktop. Fix:
1. Press `Win + R`, run `services.msc`.
2. Double click **Jenkins** -> **Log On** tab -> "This account" -> enter your own Windows user and password.
3. Right click Jenkins -> **Restart**. (Docker Desktop must already be running.)

### 2.3 Jenkins plugins
Manage Jenkins -> Plugins -> Available. Make sure these are installed:
- Docker Pipeline
- GitHub (comes with the suggested plugins)
- Pipeline, Git, Credentials Binding (also suggested plugins)

### 2.4 AWS
1. In the AWS console go to IAM -> Users -> Create user, for example `jenkins-deployer`.
2. Give it permissions. For a learning account the simplest is `AdministratorAccess`. Delete the user/keys after the demo.
3. Open the user -> Security credentials -> Create access key (use case: "Third-party service" or "Other"). Copy the Access key ID and Secret access key. Don't put them in Git, ever.

### 2.5 Store the AWS keys in Jenkins
Manage Jenkins -> Credentials -> System -> Global credentials -> Add Credentials:
- Kind: **Username with password**
- Username: your AWS Access key ID
- Password: your AWS Secret access key
- ID: `aws-creds` (the Jenkinsfile expects exactly this)

### 2.6 Region
The Jenkinsfile deploys to `ap-south-1` (Mumbai). Change `AWS_DEFAULT_REGION` at the top of the Jenkinsfile if you want another region.

## 3. Put the code on GitHub
Replace your old project folder with this one (the code now lives under `src/calculator/`, so delete the old top level `calculator/` folder). Then:
```
git add .
git commit -m "Calculator with Lambda, SAM template and Docker pipeline"
git push origin main
```
If your branch is called `master` instead of `main`, either rename it (`git branch -M main`) or change the branch check in the Jenkinsfile.

Before pushing, a quick local check:
```
pip install -r requirements-dev.txt
python -m pytest
```

## 4. Create the Jenkins job
1. New Item -> name `calculator-pipeline` -> **Pipeline** -> OK.
2. Build Triggers: tick **GitHub hook trigger for GITScm polling**.
3. Pipeline section:
   - Definition: **Pipeline script from SCM**
   - SCM: Git
   - Repository URL: your GitHub repo URL (if it is private, add a GitHub personal access token as a credential)
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
4. Save, then click **Build Now** once.

First build takes a few minutes because Docker has to build the image and install the SAM CLI. Later builds are much faster.

**If the first build fails right at the start** with an error about the working directory being invalid or a `C:\...` path, that is the Docker Pipeline plugin not liking a Windows host. Change Script Path to `Jenkinsfile.windows` and build again. It does the same thing by calling docker directly.

Expected result of a good run: Unit tests -> Build package -> SAM build -> Deploy to AWS all green, and the log ends with a **Stack outputs** table containing `CalculatorApiUrl`.

## 5. GitHub webhook
Jenkins is on your laptop, so GitHub can't reach it. A tunnel fixes that.
1. Install ngrok and sign up for a free account, then add your auth token (`ngrok config add-authtoken <token>`).
2. Run: `ngrok http 8080` (8080 is Jenkins' default port) and copy the `https://....ngrok-free.app` address.
3. On GitHub: repo -> Settings -> Webhooks -> Add webhook
   - Payload URL: `https://<your-ngrok-address>/github-webhook/` (keep the trailing slash)
   - Content type: `application/json`
   - Events: Just the push event
4. GitHub shows a green tick on the first delivery if it worked (Recent Deliveries tab).

The free ngrok address changes every time you restart ngrok, so update the webhook URL before each demo.

## 6. Test the deployed API
Use `curl.exe` in PowerShell (plain `curl` there is something different). Put in your own `CalculatorApiUrl`:
```
curl.exe "https://<id>.execute-api.ap-south-1.amazonaws.com/Prod/calculate?operation=add&a=10&b=5"
curl.exe "https://<id>.execute-api.ap-south-1.amazonaws.com/Prod/calculate?operation=multiply&a=6&b=7"
curl.exe "https://<id>.execute-api.ap-south-1.amazonaws.com/Prod/calculate?operation=add&a=-4&b=5"
```
Expected: `{"operation": "add", "a": 10, "b": 5, "result": 15}`, then 42, then a 400 error saying a must be a positive integer.

POST version:
```
curl.exe -X POST "https://<id>.execute-api.ap-south-1.amazonaws.com/Prod/calculate" -H "Content-Type: application/json" -d "{\"operation\":\"subtract\",\"a\":10,\"b\":4}"
```

## 7. Demo script (commit to cloud)
1. Show GitHub repo, Jenkins job and the AWS CloudFormation console (the stack already exists from the first run).
2. Make a small visible change, e.g. in `handler.py` add a field to the success response, commit and push.
3. Switch to Jenkins: a new build starts by itself (webhook).
4. Walk through the stages as they go green: tests, package build, SAM build, deploy.
5. In AWS: CloudFormation -> `calculator-stack` -> status UPDATE_COMPLETE, then Lambda console shows the new code.
6. Call the API with curl and show the change in the response.
7. Show a bad input (`a=-4`) returning 400.

## 8. What the assignment points map to

| Assignment item | Where |
|---|---|
| Jenkins + Docker configured | sections 2.1 - 2.3 |
| Calculator (add, subtract, multiply, positive ints) | `src/calculator/operations.py` |
| Python package with unit tests | `src/`, `tests/`, `pyproject.toml` |
| CloudFormation / SAM template | `template.yaml` |
| GitHub webhook triggers Jenkins | section 5 |
| Pipeline with Docker agent: CI (test, build) and CD (deploy) | `Jenkinsfile`, `Dockerfile` |

## 9. Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| `docker: command not found` in Jenkins | Docker Desktop not running, or Jenkins wasn't restarted after installing Docker |
| `error during connect ... docker_engine` | Jenkins service still running as SYSTEM, do step 2.2 |
| Working directory invalid / `C:\` path error | Use `Jenkinsfile.windows` |
| `Could not find credentials 'aws-creds'` | Credential ID typed differently, must be exactly `aws-creds` |
| `AccessDenied` / `not authorized` during deploy | IAM user lacks permissions (CloudFormation, Lambda, API Gateway, IAM, S3) |
| Deploy stage skipped | Branch isn't `main`. Check the `when` condition in the Jenkinsfile |
| Webhook shows 403 or timeout | ngrok not running, URL changed, or missing trailing slash on `/github-webhook/` |
| Webhook OK but no build starts | "GitHub hook trigger for GITScm polling" not ticked, or wrong branch in the job |
| Stack stuck in ROLLBACK_COMPLETE after a failed first deploy | `sam delete --stack-name calculator-stack --region ap-south-1`, then rebuild |

## 10. Clean up after the demo
```
sam delete --stack-name calculator-stack --region ap-south-1
```
Then delete the IAM access keys and stop ngrok.
