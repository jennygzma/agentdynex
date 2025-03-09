import { Card, Paper, Stack, Tab, Tabs, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { TreeNode, useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";

const ConfigCreation = () => {
  const {
    updateIsLoading,
    currentPrototype,
    updateCurrentRunId,
    currentRunTree,
    updateCurrentRunTree,
  } = useAppContext();
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

  const createNewRun = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/create_new_run`,
    })
      .then((response) => {
        console.log("/create_new_run request successful:", response.data);
        getRunTree();
        updateCurrentRunId(response.data.new_run_id);
      })
      .catch((error) => {
        console.error("Error calling /create_new_run request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

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

  useEffect(() => {
    if (!currentPrototype) return;
    getConfig();
    getRunTree();
  }, [currentPrototype]);

  if (!currentPrototype) return <></>;
  return (
    <Stack spacing="10px" width="100%">
      {config ? (
        <Stack direction="row" spacing="10px">
          {!currentRunTree && (
            <Button
              onClick={generateConfig}
              sx={{
                width: "100%",
              }}
            >
              Regenerate Config
            </Button>
          )}
          <Button
            onClick={() => {
              createNewRun();
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
