import { Divider, Stack, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { TreeNode, useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import Fixes from "./fixes";
import UserSpecifiedFixes from "./user-specified-fixes";

const Reflection = () => {
  const {
    updateIsLoading,
    currentPrototype,
    currentRunId,
    updateCurrentRunId,
    updateCurrentRunTree,
  } = useAppContext();
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
        type: "updated",
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
        type: "updated",
      },
    })
      .then((response) => {
        console.log("/get_config request successful:", response.data);
        setConfig(response.data.config ?? "");
      })
      .catch((error) => {
        console.error("Error calling /get_config request:", error);
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

  const generateUpdatedConfig = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/generate_updated_config`,
    })
      .then((response) => {
        console.log(
          "/generate_updated_config request successful:",
          response.data,
        );
      })
      .catch((error) => {
        console.error("Error calling /generate_updated_config request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
        getConfig();
      });
  };

  useEffect(() => {
    if (!currentPrototype) return;
    getRunTree();
    getConfig();
  }, [currentPrototype, currentRunId]);

  // if (!config) return <></>;
  if (!expand) {
    return (
      <Stack direction="row" spacing="10px">
        <Button onClick={() => setExpand(true)}>
          <ExpandMore />
        </Button>
        <Typography variant="h5" sx={{ fontWeight: "bold" }}>
          HOLISTIC REFLECTION
        </Typography>
      </Stack>
    );
  }
  return (
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
          HOLISTIC REFLECTION
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
            Recommended Fixes
          </Typography>
          <Fixes />
          <Divider />
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            User Specified Errors
          </Typography>
          <UserSpecifiedFixes />
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
            {config && (
              <Button
                onClick={() => {
                  createNewRun();
                }}
              >
                Create New Run ➕
              </Button>
            )}
          </Stack>
          <Stack spacing="10px">
            <Button
              onClick={() => {
                generateUpdatedConfig();
              }}
            >
              APPLY FIXES AND GENERATE NEW CONFIG
            </Button>
            <TextField
              className={"updated_config"}
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
        </Stack>
      </Stack>
    </Stack>
  );
};

export default Reflection;
