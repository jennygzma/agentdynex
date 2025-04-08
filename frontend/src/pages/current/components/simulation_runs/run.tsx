import {
  Divider,
  Stack,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { TreeNode, useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";
import Reflection from "./reflection";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import ContinuousData from "./continuous-data";

const Run = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

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
  const [updatedConfig, setUpdatedConfig] = useState(false);
  const [hasReflection, setHasReflection] = useState(false);
  const [expand, setExpand] = useState(true);
  const [simulationDataExpand, setSimulationDataExpand] = useState(true);
  const [status, setStatus] = useState("");
  const [contentHeight, setContentHeight] = useState(50);

  // Responsive rows calculation for text fields
  useEffect(() => {
    const calculateRows = () => {
      const windowHeight = window.innerHeight;
      // Adjust rows based on window height
      const newRows = Math.max(20, Math.floor(windowHeight / 30));
      setContentHeight(newRows);
    };

    // Calculate on mount
    calculateRows();

    // Add resize listener
    window.addEventListener("resize", calculateRows);

    // Cleanup listener on unmount
    return () => window.removeEventListener("resize", calculateRows);
  }, []);

  const getStatus = useCallback(() => {
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
      });
  }, []);

  const getRunTree = useCallback(() => {
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
  }, [updateIsLoading, updateCurrentRunTree]);

  const runSimulation = useCallback(() => {
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
  }, [updateIsLoading, getRunTree]);

  const stopSimulation = useCallback(() => {
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
  }, [updateIsLoading]);

  const saveConfig = useCallback(() => {
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
  }, [config, updateIsLoading]);

  const getConfig = useCallback(() => {
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
  }, [updateIsLoading]);

  const generateSummary = useCallback(() => {
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
  }, [updateIsLoading]);

  const getLogs = useCallback(() => {
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
  }, [updateIsLoading]);

  const getSummary = useCallback(() => {
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
  }, [updateIsLoading]);

  useEffect(() => {
    if (isRunningSimulation) {
      const statusIntervalId = setInterval(getStatus, 30000);
      return () => {
        clearInterval(statusIntervalId);
      };
    }
  }, [isRunningSimulation, getStatus]);

  useEffect(() => {
    if (!currentPrototype) return;
    getConfig();
    getLogs();
    getSummary();
    setExpand(true);
    setStatus("");
  }, [currentPrototype, currentRunId, getConfig, getLogs, getSummary]);
  if (!currentPrototype) return null;

  return (
    <Stack spacing="20px" width="100%" maxWidth="100%" overflow="hidden">
      {!expand ? (
        <Stack direction="row" spacing="10px">
          <Button onClick={() => setExpand(true)}>
            <ExpandMore />
          </Button>
          <Typography variant="h5" sx={{ fontWeight: "bold" }}>
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
              variant="h5"
              sx={{
                fontWeight: "bold",
              }}
            >
              SIMULATION RUN
            </Typography>
          </Stack>
          <Stack spacing="20px" direction={isMobile ? "column" : "row"}>
            {isRunningSimulation ? (
              <Stack
                direction={isMobile ? "column" : "row"}
                spacing="20px"
                sx={{ alignItems: isMobile ? "flex-start" : "center" }}
                width="100%"
              >
                <img
                  src={require("../../../../assets/robin-beginning.gif")}
                  style={{ width: "30px", height: "25px" }}
                  alt="robin running"
                />
                <Typography variant="h6" sx={{ fontFamily: "courier" }}>
                  Running Simulation...
                </Typography>
                <Button
                  onClick={() => {
                    updateIsRunningSimulation(false);
                    stopSimulation();
                  }}
                >
                  Stop Running Simulation
                  <img
                    src={require("../../../../assets/robin-kid.gif")}
                    style={{ width: "35px", height: "25px", marginLeft: "5px" }}
                    alt="stop"
                  />
                </Button>
                <Stack
                  width={isMobile ? "100%" : "75%"}
                  spacing="10px"
                  direction="row"
                  sx={{ alignItems: "center" }}
                >
                  <Typography
                    variant="body1"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    Status
                  </Typography>
                  <TextField
                    className={"Status"}
                    rows={1}
                    value={status}
                    readOnly={true}
                    code={true}
                  />
                </Stack>
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
            {!isRunningSimulation && (
              <Button
                onClick={() => {
                  setHasReflection(true);
                  setExpand(false);
                }}
              >
                REFLECT
              </Button>
            )}
          </Stack>
          <Stack spacing="20px">
            <ContinuousData parentExpand={expand} />
            {!simulationDataExpand ? (
              <Stack direction="row" spacing="10px">
                <Button onClick={() => setSimulationDataExpand(true)}>
                  <ExpandMore />
                </Button>
                <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                  SIMULATION DATA
                </Typography>
              </Stack>
            ) : (
              <Stack spacing="20px">
                <Stack direction="row" spacing="10px">
                  <Button onClick={() => setSimulationDataExpand(false)}>
                    <ExpandLess />
                  </Button>
                  <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                    SIMULATION DATA
                  </Typography>
                </Stack>
                <Stack
                  spacing="20px"
                  width="100%"
                  direction={isMobile ? "column" : "row"}
                  sx={{ overflow: "hidden" }}
                >
                  {
                    <Stack spacing="25px" width="100%" sx={{ minWidth: 0 }}>
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
                        rows={contentHeight}
                        value={config}
                        onChange={(e) => {
                          setConfig(e.target.value);
                          setUpdatedConfig(true);
                        }}
                        code={true}
                        sx={{ maxWidth: "100%" }}
                      />
                      <Button
                        disabled={!updatedConfig}
                        onClick={saveConfig}
                        sx={{ width: "100%" }}
                      >
                        Update Config
                      </Button>
                    </Stack>
                  }
                  {(isRunningSimulation || logs) && (
                    <Stack width="100%" spacing="20px" sx={{ minWidth: 0 }}>
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
                        rows={contentHeight}
                        value={logs}
                        readOnly={true}
                        code={true}
                        sx={{ maxWidth: "100%" }}
                      />
                    </Stack>
                  )}
                  {
                    <Stack width="100%" spacing="20px" sx={{ minWidth: 0 }}>
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
                          Summary
                        </Typography>
                        {logs && (
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
                        rows={contentHeight}
                        value={summary}
                        readOnly={true}
                        code={true}
                        sx={{ maxWidth: "100%" }}
                      />
                    </Stack>
                  }
                </Stack>
              </Stack>
            )}
          </Stack>
        </Stack>
      )}
      <Divider />
      <Reflection />
    </Stack>
  );
};

export default Run;
