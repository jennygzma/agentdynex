import {
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import InputWithButton from "../../../../components/InputWithButton";
import { useAppContext } from "../../hooks/app-context";
import Category from "./category";
import { CategoryType, useMatrixContext } from "../../hooks/matrix-context";
import { SERVER_URL } from "../..";

const MATRIX_CATEGORY_DESCRIPTIONS: Record<CategoryType, string> = {
  AgentsXIdea: "Who are the agent types?",
  AgentsXGrounding:
    "What are the agent's personalities? What is their role in the simulation?",
  ActionsXIdea: "What actions will the agents do?",
  ActionsXGrounding:
    "How can we translate these actions to work in a simulation? What mechanisms are necessary?",
  WorldXIdea: "What is the world the agents interact in?",
  WorldXGrounding:
    "How should we define each room? What do agents do in each room?",
};

const getDependencies = (
  category: CategoryType | undefined,
  matrixCategoryInfo: Record<CategoryType, string | []>,
): CategoryType[] => {
  let dependencies = [];
  if (category === undefined) return dependencies;
  Object.entries(matrixCategoryInfo).forEach(([key, value]) => {
    if (value.length > 0) dependencies.push(key);
  });

  const isIdea = category?.includes("Idea");
  if (isIdea) {
    const col = category.split("X")[0];
    dependencies = dependencies.filter((d) => !d?.includes(col));
  } else {
    dependencies = dependencies.filter((d) => d !== category);
  }
  return dependencies;
};

const Matrix = () => {
  const {
    currentPrototype,
    updateCurrentPrototype,
    updateIsLoading,
    updatePrototypes,
  } = useAppContext();
  const {
    submittedProblem,
    updateSubmittedProblem,
    updatedMatrix,
    updateUpdatedMatrix,
    currentCategory,
    matrixCategoryInfo,
    updateCurrentCategory,
  } = useMatrixContext();
  const [problem, setProblem] = useState("");
  const [prototypeName, setPrototypeName] = useState("");
  const [dependencies, setDependencies] = useState([]);

  useEffect(() => {
    setDependencies(getDependencies(currentCategory, matrixCategoryInfo));
  }, [currentCategory]);

  const getProblem = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_problem`,
    })
      .then((response) => {
        console.log("/get_problem request successful:", response.data);
        if (response.data.problem) {
          setProblem(response.data.problem);
          updateSubmittedProblem(true);
        }
      })
      .catch((error) => {
        console.error("Error calling /get_problem request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getPrototypeName = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_prototype_name`,
    })
      .then((response) => {
        console.log("/get_prototype_name request successful:", response.data);
        setPrototypeName(response.data.prototype_name);
      })
      .catch((error) => {
        console.error("Error calling /get_prototype_name request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const saveProblem = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/save_problem`,
      data: {
        problem: problem,
      },
    })
      .then((response) => {
        console.log("/save_problem request successful:", response.data);
        updateSubmittedProblem(true);
      })
      .catch((error) => {
        console.error("Error calling /save_problem request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const explorePrototype = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/explore_prototype`,
      data: {
        prototype: prototypeName,
      },
    })
      .then((response) => {
        console.log("/explore_prototype request successful:", response.data);
        getPrototypes();
      })
      .catch((error) => {
        console.error("Error calling /explore_prototype request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getPrototypes = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_prototypes`,
    })
      .then((response) => {
        console.log("/get_prototypes request successful:", response.data);
        updatePrototypes(response.data.prototypes);
      })
      .catch((error) => {
        console.error("Error calling /get_prototypes request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
    getProblem();
    getPrototypes();
  }, []);

  useEffect(() => {
    getPrototypeName();
  }, [currentPrototype]);

  return (
    <Stack
      spacing="10px"
      sx={{
        paddingY: "120px",
        paddingX: "40px",
      }}
    >
      <InputWithButton
        className="problem"
        label="Problem"
        input={problem}
        setInput={setProblem}
        onClick={saveProblem}
      />
      {submittedProblem && (
        <>
          <TableContainer sx={{ backgroundColor: "white" }}>
            <Table
              sx={{
                borderCollapse: "collapse",
              }}
            >
              <TableHead>
                <TableRow>
                  <TableCell
                    sx={{ width: "7%", borderBottom: "none" }}
                  ></TableCell>
                  <TableCell
                    sx={{
                      width: "31%",
                      borderBottom: "none",
                      verticalAlign: "bottom",
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: "bold",
                      }}
                    >
                      AGENTS
                    </Typography>
                  </TableCell>
                  <TableCell
                    sx={{
                      width: "31%",
                      borderBottom: "none",
                      verticalAlign: "bottom",
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: "bold",
                      }}
                    >
                      ACTIONS
                    </Typography>
                  </TableCell>
                  <TableCell
                    sx={{
                      width: "31%",
                      borderBottom: "none",
                      verticalAlign: "bottom",
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: "bold",
                      }}
                    >
                      WORLD
                    </Typography>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell
                    align="right"
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: "bold",
                      }}
                    >
                      IDEA
                    </Typography>
                  </TableCell>
                  <TableCell
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Category
                      category={"AgentsXIdea"}
                      description={MATRIX_CATEGORY_DESCRIPTIONS["AgentsXIdea"]}
                      isDependency={dependencies?.includes("AgentsXIdea")}
                    />
                  </TableCell>
                  <TableCell
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Category
                      category={"ActionsXIdea"}
                      description={MATRIX_CATEGORY_DESCRIPTIONS["ActionsXIdea"]}
                      isDependency={dependencies?.includes("ActionsXIdea")}
                    />
                  </TableCell>
                  <TableCell
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Category
                      category={"WorldXIdea"}
                      description={MATRIX_CATEGORY_DESCRIPTIONS["WorldXIdea"]}
                      isDependency={dependencies?.includes("WorldXIdea")}
                    />
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell
                    align="right"
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        fontWeight: "bold",
                      }}
                    >
                      GROUNDING
                    </Typography>
                  </TableCell>
                  <TableCell
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Category
                      category="AgentsXGrounding"
                      description={
                        MATRIX_CATEGORY_DESCRIPTIONS["AgentsXGrounding"]
                      }
                      isDependency={dependencies?.includes("AgentsXGrounding")}
                    />
                  </TableCell>
                  <TableCell
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Category
                      category="ActionsXGrounding"
                      description={
                        MATRIX_CATEGORY_DESCRIPTIONS["ActionsXGrounding"]
                      }
                      isDependency={dependencies?.includes("ActionsXGrounding")}
                    />
                  </TableCell>
                  <TableCell
                    sx={{
                      borderBottom: "none",
                      verticalAlign: "top",
                    }}
                  >
                    <Category
                      category="WorldXGrounding"
                      description={
                        MATRIX_CATEGORY_DESCRIPTIONS["WorldXGrounding"]
                      }
                      isDependency={dependencies?.includes("WorldXGrounding")}
                    />
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
          <InputWithButton
            className="prototyp-name"
            label="Prototype Name"
            input={prototypeName}
            setInput={setPrototypeName}
            onClick={() => {
              explorePrototype();
              updateUpdatedMatrix(false);
              updateCurrentPrototype(prototypeName);
            }}
            onChange={() => {
              updateCurrentCategory(undefined);
            }}
            direction="row"
            buttonName="Explore Prototype"
            disabled={!updatedMatrix}
          />
        </>
      )}
    </Stack>
  );
};

export default Matrix;
