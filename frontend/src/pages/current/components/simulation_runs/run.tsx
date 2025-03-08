import {
  Card,
  Divider,
  Paper,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";
import Reflection from "./reflection";
import { ExpandLess, ExpandMore } from "@mui/icons-material";

const Run = () => {
  const { updateIsLoading, currentPrototype } = useAppContext();
  const [config, setConfig] = useState("");
  const [updatedConfig, setUpdatedConfig] = useState(false);
  const [isRunningSimulation, setIsRunningSimulation] = useState(false);
  const [hasLogs, setHasLogs] = useState(false);
  const [hasReflection, setHasReflection] = useState(true);
  const [expand, setExpand] = useState(true);

  const saveConfig = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/save_config`,
      data: {
        config,
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

  const generateConfig = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/generate_config`,
    })
      .then((response) => {
        console.log("/generate_config request successful:", response.data);
        getConfig();
      })
      .catch((error) => {
        console.error("Error calling /generate_config request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
    if (!currentPrototype) return;
    getConfig();
  }, [currentPrototype]);

  if (!currentPrototype) return <></>;
  return (
    <Stack spacing="20px" width="85%">
      {hasReflection && <Reflection />}
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
              <Button
                onClick={() => {
                  setIsRunningSimulation(false);
                  // call endpoint to stop simulation
                }}
              >
                Stop Running Simulation
              </Button>
            ) : (
              <Button
                onClick={() => {
                  setIsRunningSimulation(true);
                  // call endpoint to run simulation
                }}
              >
                Run Simulation
              </Button>
            )}
            {!isRunningSimulation && hasLogs && (
              <Button
                onClick={() => {
                  setHasReflection(true);
                  // call endpoint to reflect on stuff
                }}
              >
                REFLECT
              </Button>
            )}
          </Stack>
          <Stack spacing="20px" width="100%" direction="row">
            {config && (
              <Stack spacing="10px" width="33%">
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
                  rows={75}
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
            <Stack width="33%">
              <Typography
                variant="h6"
                sx={{
                  fontWeight: "bold",
                }}
              >
                Logs
              </Typography>
              <TextField
                className={"Logs"}
                value={"LOGLOGLOGFILLIN LATER"}
                readOnly={true}
                code={true}
              />
            </Stack>
            <Stack width="33%">
              <Typography
                variant="h6"
                sx={{
                  fontWeight: "bold",
                }}
              >
                Summary
              </Typography>
              <TextField
                className={"Summary"}
                value={"SUMMARY FILL IN LATER"}
                readOnly={true}
                code={true}
              />
            </Stack>
          </Stack>
        </Stack>
      )}
    </Stack>
  );
};

export default Run;
