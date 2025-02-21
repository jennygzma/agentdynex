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
import { useAppContext } from "../hooks/app-context";
import { CategoryType, useMatrixContext } from "../hooks/matrix-context";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import Button from "../../../components/Button";
import { SERVER_URL } from "..";

const MATRIX_CATEGORY_DESCRIPTIONS: Record<CategoryType, string> = {
  AgentsXIdea: "Who is the application for?",
  AgentsXGrounding:
    "What is the users goal? What are problems with existing approaches?",
  ActionsXIdea:
    "What is the concept, theory, or strategy that guides the solution?",
  ActionsXGrounding: "How do we translate this approach to reality?",
  WorldXIdea: "What is the core interaction paradigm?",
  WorldXGrounding: "What are the core features for this interaction?",
};

const Matrix = () => {
  const {
    currentPrototype,
    updateCurrentPrototype,
    updateIsLoading,
    updatePrototypes,
  } = useAppContext();
  const [problem, setProblem] = useState("");
  const [prototypeName, setPrototypeName] = useState("");
  const [expand, setExpand] = useState(true);

  const [AgentsXIdea, setAgentsXIdea] = useState("");
  const [ActionsXIdea, setActionsXIdea] = useState("");
  const [WorldXIdea, setWorldXIdea] = useState("");
  const [AgentsXGrounding, setAgentsXGrounding] = useState("");
  const [ActionsXGrounding, setActionsXGrounding] = useState("");
  const [WorldXGrounding, setWorldXGrounding] = useState("");

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
    const fetchInput = async () => {
      updateIsLoading(true);
      try {
        const agentsXIdea = await getInput("AgentsXIdea");
        setAgentsXIdea(agentsXIdea);
        const actionsXIdea = await getInput("ActionsXIdea");
        setActionsXIdea(actionsXIdea);
        const worldXIdea = await getInput("WorldXIdea");
        setWorldXIdea(worldXIdea);
        const agentsXGrounding = await getInput("AgentsXGrounding");
        setAgentsXGrounding(agentsXGrounding);
        const actionsXGrounding = await getInput("ActionsXGrounding");
        setActionsXGrounding(actionsXGrounding);
        const worldXGrounding = await getInput("WorldXGrounding");
        setWorldXGrounding(worldXGrounding);
      } catch (error) {
        console.error("Failed to fetch input:", error);
      } finally {
        updateIsLoading(false);
      }
    };
    fetchInput();
  }, [currentPrototype]);

  const getInput = async (category: string): Promise<string | undefined> => {
    try {
      const response = await axios({
        method: "GET",
        url: `${SERVER_URL}/get_input`,
        params: {
          category: category,
        },
      });
      console.log("/get_input request successful:", response.data);
      return response.data.input;
    } catch (error) {
      console.error("Error calling /get_input request:", error);
    }
  };

  if (!expand) {
    return (
      <Stack
        direction="row"
        spacing="10px"
        sx={{
          alignItems: "center",
          paddingTop: "100px",
        }}
      >
        <Button onClick={() => setExpand(true)}>
          <ExpandMore />
        </Button>
        <Typography variant="h5" sx={{ fontWeight: "bold" }}>
          DESIGN MATRIX CONTEXT
        </Typography>
      </Stack>
    );
  }
  return (
    <Stack
      spacing="10px"
      sx={{
        paddingTop: "100px",
      }}
    >
      <Stack
        direction="row"
        spacing="10px"
        sx={{
          alignItems: "center",
        }}
      >
        <Button onClick={() => setExpand(false)}>
          <ExpandLess />
        </Button>
        <Typography variant="h5" sx={{ fontWeight: "bold" }}>
          DESIGN MATRIX CONTEXT
        </Typography>
      </Stack>
      <Typography variant="h6">Simulation Goal: {problem}</Typography>
      <Typography variant="h6">{currentPrototype}</Typography>
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
                      //fontFamily: "monospace",
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
                      // fontFamily: "monospace",
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
                      // fontFamily: "monospace",
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
                      // fontFamily: "monospace",
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
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    {MATRIX_CATEGORY_DESCRIPTIONS["AgentsXIdea"]}
                  </Typography>
                  <Typography variant="body2">{AgentsXIdea}</Typography>
                </TableCell>
                <TableCell
                  sx={{
                    borderBottom: "none",
                    verticalAlign: "top",
                  }}
                >
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    {MATRIX_CATEGORY_DESCRIPTIONS["ActionsXIdea"]}
                  </Typography>
                  <Typography variant="body2">{ActionsXIdea}</Typography>
                </TableCell>
                <TableCell
                  sx={{
                    borderBottom: "none",
                    verticalAlign: "top",
                  }}
                >
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    {MATRIX_CATEGORY_DESCRIPTIONS["WorldXIdea"]}
                  </Typography>
                  <Typography variant="body2">{WorldXIdea}</Typography>
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
                      // fontFamily: "monospace",
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
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    {MATRIX_CATEGORY_DESCRIPTIONS["AgentsXGrounding"]}
                  </Typography>
                  <Typography variant="body2">{AgentsXGrounding}</Typography>
                </TableCell>
                <TableCell
                  sx={{
                    borderBottom: "none",
                    verticalAlign: "top",
                  }}
                >
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    {MATRIX_CATEGORY_DESCRIPTIONS["ActionsXGrounding"]}
                  </Typography>
                  <Typography variant="body2">{ActionsXGrounding}</Typography>
                </TableCell>
                <TableCell
                  sx={{
                    borderBottom: "none",
                    verticalAlign: "top",
                  }}
                >
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    {MATRIX_CATEGORY_DESCRIPTIONS["WorldXGrounding"]}
                  </Typography>
                  <Typography variant="body2">{WorldXGrounding}</Typography>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </>
    </Stack>
  );
};

export default Matrix;
