import { Divider, Stack, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { TreeNode, useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";
import Reflection from "./reflection";
import { ExpandLess, ExpandMore } from "@mui/icons-material";

const Run = () => {
  const {
    updateIsLoading,
    currentPrototype,
    currentRunId,
    isRunningSimulation,
    updateIsRunningSimulation,
    updateCurrentRunTree,
  } = useAppContext();
  const [config, setConfig] = useState("");
  const [logs, setLogs] = useState("");
  const [summary, setSummary] = useState("");
  const [status, setStatus] = useState("");
  const [milestones, setMilestones] = useState("");
  const [updatedConfig, setUpdatedConfig] = useState(false);
  // const [isRunningSimulation, setIsRunningSimulation] = useState(false);
  const [hasReflection, setHasReflection] = useState(false);
  const [expand, setExpand] = useState(true);

  const getRunTree = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_run_tree`,
    })
      .then((response) => {
        console.log("/get_run_tree request successful:", response.data);
        const runTreeJSON = response.data.run_tree;
        function transformToTreeNode(response: any): TreeNode {
          const treeNode: TreeNode = {};
          for (const key in response) {
            if (response.hasOwnProperty(key)) {
              treeNode[key] = Object.keys(response[key]).length
                ? transformToTreeNode(response[key])
                : undefined;
            }
          }
          return treeNode;
        }
        const runTree = transformToTreeNode(runTreeJSON);
        updateCurrentRunTree(runTree);
      })
      .catch((error) => {
        console.error("Error calling /get_run_tree request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const runSimulation = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/run_simulation`,
    })
      .then((response) => {
        console.log("/run_simulation request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /run_simulation request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
        getRunTree();
      });
  };

  const stopSimulation = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/stop_simulation`,
    })
      .then((response) => {
        console.log("/stop_simulation request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /stop_simulation request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const saveConfig = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/save_config`,
      data: {
        config,
        type: "initial",
      },
    })
      .then((response) => {
        console.log("/save_config request successful:", response.data);
        getConfig();
        setUpdatedConfig(false);
      })
      .catch((error) => {
        console.error("Error calling /save_config request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getConfig = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_config`,
      params: {
        type: "initial",
      },
    })
      .then((response) => {
        console.log("/get_config request successful:", response.data);
        setConfig(response.data.config);
      })
      .catch((error) => {
        console.error("Error calling /get_config request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const generateSummary = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/generate_summary`,
    })
      .then((response) => {
        console.log("/generate_summary request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /generate_summary request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
        getSummary();
      });
  };

  const getLogs = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_logs`,
    })
      .then((response) => {
        console.log("/get_logs request successful:", response.data);
        setLogs(response.data.logs);
      })
      .catch((error) => {
        console.error("Error calling /get_logs request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getSummary = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_summary`,
    })
      .then((response) => {
        console.log("/get_summary request successful:", response.data);
        setSummary(response.data.summary);
      })
      .catch((error) => {
        console.error("Error calling /get_summary request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getMilestones = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_milestones`,
    })
      .then((response) => {
        console.log("/get_milestones request successful:", response.data);
        setMilestones(response.data.milestones);
      })
      .catch((error) => {
        console.error("Error calling /get_milestones request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getStatus = () => {
    // updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_status`,
    })
      .then((response) => {
        console.log("/get_status request successful:", response.data);
        setStatus(response.data.status);
      })
      .catch((error) => {
        console.error("Error calling /get_status request:", error);
      })
      .finally(() => {
        // updateIsLoading(false);
      });
  };

  const getAnalysis = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_analysis`,
    })
      .then((response) => {
        console.log("/get_analysis request successful:", response.data);
        setHasReflection(response.data.analysis ? true : false);
      })
      .catch((error) => {
        console.error("Error calling /get_analysis request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
    if (!currentPrototype) return;
    getConfig();
    getAnalysis();
    getLogs();
    getSummary();
    setExpand(true);
    setStatus("");
    setMilestones("");
  }, [currentPrototype, currentRunId]);

  useEffect(() => {
    if (isRunningSimulation) {
      const intervalId = setInterval(getStatus, 30000);
      return () => clearInterval(intervalId);
    }
  }, [isRunningSimulation]);

  if (!currentPrototype) return <></>;
  return (
    <Stack spacing="20px" width="85%">
      {!expand ? (
        <Stack direction="row" spacing="10px">
          <Button onClick={() => setExpand(true)}>
            <ExpandMore />
          </Button>
          <Typography variant="h6" sx={{ fontWeight: "bold" }}>
            SIMULATION RUN
          </Typography>
        </Stack>
      ) : (
        <Stack spacing="20px">
          <Stack direction="row" spacing="10px">
            <Button onClick={() => setExpand(false)}>
              <ExpandLess />
            </Button>
            <Typography
              variant="h6"
              sx={{
                fontWeight: "bold",
              }}
            >
              SIMULATION RUN
            </Typography>
          </Stack>
          <Stack spacing="20px" direction="row">
            {isRunningSimulation ? (
              <Stack
                direction="row"
                spacing="10px"
                sx={{ alignItems: "center" }}
              >
                <Typography variant="h6">Running Simulation...</Typography>
                <img
                  src={require("../../../../assets/robin-beginning.gif")}
                  style={{ width: "30px", height: "25px" }}
                  alt="robin running"
                />
                <Button
                  onClick={() => {
                    updateIsRunningSimulation(false);
                    stopSimulation();
                  }}
                >
                  Stop Running Simulation&nbsp;&nbsp;
                  <img
                    src={require("../../../../assets/robin-kid.gif")}
                    style={{ width: "35px", height: "25px" }}
                    alt="stop"
                  />
                </Button>{" "}
              </Stack>
            ) : (
              <Button
                onClick={() => {
                  updateIsRunningSimulation(true);
                  runSimulation();
                }}
              >
                {logs ? "Rerun Simulation" : "Run Simulation"}&nbsp;&nbsp;
                <img
                  src={require("../../../../assets/robin-beginning.gif")}
                  style={{ width: "30px", height: "25px" }}
                  alt="run"
                />
              </Button>
            )}
            {!isRunningSimulation && logs && summary && (
              <Button
                onClick={() => {
                  setHasReflection(true);
                  setExpand(false);
                  // generateReflection();
                }}
              >
                REFLECT
              </Button>
            )}
          </Stack>
          <Stack spacing="20px" width="100%" direction="row">
            {config && (
              <Stack spacing="25px" width="100%">
                <Typography
                  variant="h6"
                  sx={{
                    fontWeight: "bold",
                  }}
                >
                  Original Configuration
                </Typography>
                <TextField
                  className={"code"}
                  rows={50}
                  value={config}
                  onChange={(e) => {
                    setConfig(e.target.value);
                    setUpdatedConfig(true);
                  }}
                  code={true}
                />
                <Button
                  disabled={!updatedConfig}
                  onClick={saveConfig}
                  sx={{ width: "100%" }}
                >
                  Update Config
                </Button>
              </Stack>
            )}
            {(isRunningSimulation || logs) && (
              <Stack width="100%" spacing="20px">
                <Stack direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    Milestones
                  </Typography>
                  <Button onClick={() => getMilestones()}>
                    GET MILESTONES
                  </Button>
                </Stack>
                <TextField
                  className={"Milestones"}
                  rows={5}
                  value={milestones}
                  readOnly={true}
                  code={true}
                />
                <Divider />
                {isRunningSimulation && (
                  <>
                    <Stack
                      direction="row"
                      sx={{ justifyContent: "space-between" }}
                    >
                      <Typography
                        variant="h6"
                        sx={{
                          fontWeight: "bold",
                        }}
                      >
                        Status
                      </Typography>
                    </Stack>
                    <TextField
                      className={"Status"}
                      rows={5}
                      value={status}
                      readOnly={true}
                      code={true}
                    />
                    <Divider />
                  </>
                )}
                <Stack direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    Logs
                  </Typography>
                  <Button
                    onClick={() => {
                      getLogs();
                    }}
                  >
                    Get Logs 📝
                  </Button>
                </Stack>
                <TextField
                  className={"Logs"}
                  rows={45}
                  value={logs}
                  readOnly={true}
                  code={true}
                />
              </Stack>
            )}
            {(isRunningSimulation || logs) && (
              <Stack width="100%" spacing="20px">
                <Stack direction="row" sx={{ justifyContent: "space-between" }}>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    Summary
                  </Typography>
                  {!isRunningSimulation && logs && (
                    <Button
                      onClick={() => {
                        generateSummary();
                      }}
                    >
                      Get Summary ℹ️
                    </Button>
                  )}
                </Stack>
                <TextField
                  className={"Summary"}
                  rows={50}
                  value={summary}
                  readOnly={true}
                  code={true}
                />
              </Stack>
            )}
          </Stack>
        </Stack>
      )}
      <Divider />
      {hasReflection && <Reflection />}
    </Stack>
  );
};

export default Run;
