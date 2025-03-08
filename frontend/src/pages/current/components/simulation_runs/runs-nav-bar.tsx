import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardActionArea, Stack, Typography } from "@mui/material";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import { TreeNode, useAppContext } from "../../hooks/app-context";

const INITIAL = "initial";

const RunsNavBar = () => {
  const {
    updateIsLoading,
    currentRunId,
    updateCurrentRunId,
    // currentRunTree,
    updateCurrentRunTree,
    prototypes,
    updatePrototypes,
    currentPrototype,
    updateCurrentPrototype,
  } = useAppContext();

  const currentRunTree = {
    "run-1": {
      "run-1-1": {
        "run-1-1-1": {},
        "run-1-1-2": {},
      },
      "run-1-2": {
        "run-1-2-1": {},
        "run-1-2-2": {},
      },
      "run-1-3": {},
    },
    "run-2": {
      "run-2-1": {
        "run-2-1-1": {},
        "run-2-1-2": {},
      },
    },
  };

  const [expandedNodes, setExpandedNodes] = useState<Record<string, boolean>>(
    {},
  );

  const setCurrentRunId = (runId) => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/set_current_run_id`,
      data: {
        current_run_id: runId,
      },
    })
      .then((response) => {
        console.log("/set_current_run_id request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /set_current_run_id request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  console.log("hi jenny current_run_id" + currentRunId);

  useEffect(() => {}, [currentRunTree]);

  const toggleNode = (nodeRunId: string) => {
    setExpandedNodes((prev) => ({
      ...prev,
      [nodeRunId]: !prev[nodeRunId],
    }));
  };

  const renderTree = (tree: TreeNode, parentId = ""): JSX.Element => {
    return (
      <Stack spacing="5px">
        {Object.entries(tree).map(([key, value]) => {
          // const nodeRunId = parentId ? `${parentId}/${key}` : key;
          const nodeRunId = key;
          const isExpanded = expandedNodes[nodeRunId];

          return (
            <Stack key={nodeRunId} spacing="5px">
              <Card
                sx={{
                  fontSize: "16px",
                  boxShadow: "none",
                  borderRadius: 0,
                  border:
                    currentRunId === key
                      ? "3px solid #9d5ba3ff"
                      : "1px solid #9d5ba3ff",
                }}
              >
                <CardActionArea
                  onClick={() => {
                    updateCurrentRunId(nodeRunId);
                    setCurrentRunId(nodeRunId);
                  }}
                  sx={{ padding: "10px", borderRadius: 0 }}
                >
                  <Stack
                    direction="row"
                    sx={{ justifyContent: "space-between" }}
                  >
                    <Typography>{key}</Typography>
                    {value && Object.keys(value).length > 0 && (
                      <Button
                        colorVariant="transparent"
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleNode(nodeRunId);
                        }}
                        sx={{ padding: 0, minWidth: "0px" }}
                      >
                        {isExpanded ? "➖" : "➕"}
                      </Button>
                    )}
                  </Stack>
                </CardActionArea>
              </Card>
              {isExpanded && value && Object.keys(value).length > 0 && (
                <Stack sx={{ paddingLeft: "20px" }}>
                  {renderTree(value, nodeRunId)}
                </Stack>
              )}
            </Stack>
          );
        })}
      </Stack>
    );
  };

  if (!currentRunTree) return null;

  return (
    <Stack
      spacing="10px"
      sx={{
        padding: "10px",
        backgroundColor: "white",
        width: "15%",
        height: "100vh",
      }}
    >
      <Typography variant="h6">Runs</Typography>
      <Card
        sx={{
          fontSize: "16px",
          boxShadow: "none",
          borderRadius: 0,
          border:
            currentRunId === INITIAL
              ? "3px solid #9d5ba3ff"
              : "1px solid #9d5ba3ff",
        }}
      >
        <CardActionArea
          onClick={() => {
            updateCurrentRunId(INITIAL);
            setCurrentRunId("0");
          }}
          sx={{ padding: "10px", borderRadius: 0 }}
        >
          <Typography>{INITIAL}</Typography>
        </CardActionArea>
      </Card>
      {renderTree(currentRunTree)}
    </Stack>
  );
};

export default RunsNavBar;
