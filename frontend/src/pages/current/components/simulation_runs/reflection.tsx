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
import { ExpandLess, ExpandMore } from "@mui/icons-material";

const Reflection = () => {
  const { updateIsLoading, currentPrototype } = useAppContext();
  const [config, setConfig] = useState("");
  const [updatedConfig, setUpdatedConfig] = useState(false);
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

  const reflection = true;

  if (!reflection) return <></>;
  if (!expand) {
    return (
      <Stack direction="row" spacing="10px">
        <Button onClick={() => setExpand(true)}>
          <ExpandMore />
        </Button>
        <Typography variant="h6" sx={{ fontWeight: "bold" }}>
          REFLECTION
        </Typography>
      </Stack>
    );
  }
  return (
    <Stack>
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
          REFLECTION
        </Typography>
      </Stack>
      <Stack spacing="20px" direction="row">
        <Stack width="50%" spacing="20px">
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            Analysis
          </Typography>
          <TextField
            className={"Logs"}
            value={"LOGLOGLOGFILLIN LATER"}
            readOnly={true}
            code={true}
            rows="50"
          />
        </Stack>
        <Stack width="50%" spacing="20px">
          <Stack direction="row" sx={{ justifyContent: "space-between" }}>
            <Typography
              variant="h6"
              sx={{
                fontWeight: "bold",
              }}
            >
              Updated Configuration
            </Typography>
            <Button
              onClick={() => {
                // creating a new run
              }}
            >
              Create New Run
            </Button>
          </Stack>

          <TextField
            className={"updated_config"}
            rows={50}
            value={config}
            onChange={(e) => {
              setConfig(e.target.value);
              setUpdatedConfig(true);
            }}
            code={true}
          />
        </Stack>
      </Stack>{" "}
      <Divider />
    </Stack>
  );
};

export default Reflection;
