pipeline {
    agent any

    environment {
        DOCKER = credentials('dockerhub')
        DOCKER_REPO = "logsight/logsight-result-api"
        SONAR_PROJECT_KEY = "aiops_logsight-result-api"
        LOGSIGHT_LIB_VERSION = "v1.3.0"
        GITHUB_TOKEN = credentials('github-pat-jenkins')
    }

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.8'
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'apt-get update && apt-get install -y git-lfs'
                sh 'pip install "git+https://$GITHUB_TOKEN@github.com/aiops/logsight.git@$LOGSIGHT_LIB_VERSION"'
                sh 'PYTHONPATH=$PWD/result_api py.test --junitxml test-report.xml --cov-report xml:coverage-report.xml --cov=result_api tests/'
                stash name: 'test-reports', includes: '*.xml' 
            }
            post {
                always {
                    junit 'test-report.xml'
                    archiveArtifacts '*-report.xml'
                }
            }
        }
        stage('Linting & SonarQube') {
            parallel {
                stage('SonarQube') {
                    agent {
                        docker {
                            image 'sonarsource/sonar-scanner-cli'
                        }
                    }
                    steps {
                        script {
                            unstash "test-reports"
                            withSonarQubeEnv('logsight-sonarqube') {
                                sh """ 
                                    sonar-scanner -Dsonar.projectKey=$SONAR_PROJECT_KEY -Dsonar.branch.name=$BRANCH_NAME \
                                        -Dsonar.python.version=3 \
                                        -Dsonar.organization=logsight \
                                        -Dsonar.sources=result_api -Dsonar.tests=tests/. \
                                        -Dsonar.inclusions="**/*.py" \
                                        -Dsonar.python.coverage.reportPaths=coverage-report.xml \
                                        -Dsonar.test.reportPath=test-report.xml
                                """
                            }
                        }
                    }
                }
                stage ("Lint Dockerfile") {
                    agent {
                        docker {
                            image 'hadolint/hadolint:latest-debian'
                        }
                    }
                    steps {
                        sh 'hadolint --format json Dockerfile | tee -a hadolint.json'
                    }
                    post {
                        always {
                            archiveArtifacts 'hadolint.json'
                            recordIssues(
                                tools: [hadoLint(pattern: "hadolint.json", id: "dockerfile")]
                            )
                        }
                    }
                }
            }
        }
        stage ("Build and test Docker Image") {
            steps {
             sh """
                docker build \
                    --build-arg GITHUB_TOKEN=$GITHUB_TOKEN \
                    --build-arg LOGSIGHT_LIB_VERSION=$LOGSIGHT_LIB_VERSION \
                    -t $DOCKER_REPO:${GIT_COMMIT[0..7]} .
             """
                // Add step/script to test (amd64) docker image
            }
        }
        stage ("Build and push Docker Manifest") {
            when {
                // only run when building a tag (triggered by a release)
                // tag name = BRANCH_NAME 
                buildingTag()
            }
            steps {
                sh "docker buildx rm"
                sh "docker buildx create --driver docker-container --name multiarch --use --bootstrap"
                sh "echo $DOCKER_PSW | docker login -u $DOCKER_USR --password-stdin"
                sh """
                    docker buildx build \
                        --build-arg GITHUB_TOKEN=$GITHUB_TOKEN \
                        --build-arg LOGSIGHT_LIB_VERSION=$LOGSIGHT_LIB_VERSION \
                        --push --platform linux/amd64,linux/arm64/v8 \
                        -t $DOCKER_REPO:$BRANCH_NAME -t $DOCKER_REPO:latest .
                """
                sh "docker buildx rm"
            }
        }
    }
}