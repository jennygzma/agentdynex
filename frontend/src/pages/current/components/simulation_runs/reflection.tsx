import { Stack, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { TreeNode, useAppContext } from "../../hooks/app-context";
import { SERVER_URL } from "../..";
import Button from "../../../../components/Button";
import TextField from "../../../../components/TextField";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import InputWithButton from "../../../../components/InputWithButton";
import Fixes from "./fixes";
import UserSpecifiedFixes from "./user-specified-fixes";

type Rubric = {
  category: string;
  rubric_type: string;
  description: string;
  example: string;
};

const Reflection = () => {
  const {
    updateIsLoading,
    currentPrototype,
    currentRunId,
    updateCurrentRunId,
    updateCurrentRunTree,
  } = useAppContext();
  const [config, setConfig] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [updatedConfig, setUpdatedConfig] = useState(false);
  const [expand, setExpand] = useState(true);
  const [missingRubric, setMissingRubric] = useState<Rubric>(undefined);

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

  const getAnalysis = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_analysis`,
    })
      .then((response) => {
        console.log("/get_analysis request successful:", response.data);
        setAnalysis(response.data.analysis);
      })
      .catch((error) => {
        console.error("Error calling /get_analysis request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const generateAnalysis = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/generate_analysis`,
    })
      .then((response) => {
        console.log("/generate_analysis request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /generate_analysis request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
        getAnalysis();
        getConfig();
      });
  };

  const getMissingRubric = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_missing_rubric`,
    })
      .then((response) => {
        console.log("/get_missing_rubric request successful:", response.data);
        setMissingRubric({
          category: response.data.category,
          rubric_type: response.data.rubric_type,
          description: response.data.description,
          example: response.data.example,
        });
      })
      .catch((error) => {
        console.error("Error calling /get_missing_rubric request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const saveMissingRubric = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/add_to_rubric`,
      data: {
        config,
        category: missingRubric.category,
        rubric_type: missingRubric.rubric_type,
        description: missingRubric.description,
        example: missingRubric.example,
      },
    })
      .then((response) => {
        console.log("/add_to_rubric request successful:", response.data);
      })
      .catch((error) => {
        console.error("Error calling /add_to_rubric request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
    if (!currentPrototype) return;
    getRunTree();
    getConfig();
    getAnalysis();
  }, [currentPrototype, currentRunId]);

  const reflection = true;

  const handleRubricChange = (field: keyof Rubric, value: string) => {
    setMissingRubric((prev) => ({
      ...prev, // Preserve existing fields
      [field]: value, // Update only the specified field
    }));
  };

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
          REFLECTION
        </Typography>
      </Stack>
      <Stack spacing="20px" direction="row">
        <Stack width="50%" spacing="20px">
          {/* <Stack direction="row" sx={{ justifyContent: "space-between" }}>
            <Typography
              variant="h6"
              sx={{
                fontWeight: "bold",
              }}
            >
              Analysis
            </Typography>
            <Button
              onClick={() => {
                generateAnalysis();
              }}
            >
              Get Analysis 🤯
            </Button>
          </Stack>
          <TextField
            className={"Analysis"}
            value={analysis}
            readOnly={true}
            code={true}
            rows="50"
          /> */}
          <Fixes/>
        </Stack>
        <Stack>
          <UserSpecifiedFixes/>
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
