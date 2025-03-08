import { Card, Paper, Stack, Tab, Tabs, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";

const ConfigCreation = () => {
  const { updateIsLoading, currentPrototype } = useAppContext();
  const [config, setConfig] = useState("");
  const [updatedConfig, setUpdatedConfig] = useState(false);

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
    <Stack spacing="10px" width="100%">
      {config ? (
        <Stack direction="row" spacing="10px">
          <Button
            onClick={generateConfig}
            sx={{
              width: "100%",
            }}
          >
            Regenerate Config
          </Button>
          <Button
            onClick={() => {
              // creating a new run
            }}
            sx={{ width: "100%" }}
          >
            Create Run
          </Button>
        </Stack>
      ) : (
        <Button
          onClick={generateConfig}
          sx={{
            width: "100%",
          }}
        >
          Generate Config
        </Button>
      )}

      {config && (
        <Stack spacing="10px">
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
    </Stack>
  );
};

export default ConfigCreation;
