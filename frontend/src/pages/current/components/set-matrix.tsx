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
import { CategoryType } from "../hooks/matrix-context";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import Button from "../../../components/Button";
import { SERVER_URL } from "..";

const MATRIX_CATEGORY_DESCRIPTIONS: Record<CategoryType, string> = {
  AgentsXIdea: "Who are the agent types?",
  AgentsXGrounding:
    "What are the agent's personalities? What is their role in the simulation?",
  ActionsXIdea: "What actions will the agents do?",
  ActionsXGrounding:
    "How can we translate these actions to work in a simulation? What mechanisms are necessary?",
  LocationsXIdea: "What are the locations the agents interact in?",
  LocationsXGrounding:
    "How should we define each room? What do agents do in each room?",
  MilestonesXIdea: "What are the chronological milestones for the simulation?",
  MilestonesXGrounding:
    "What are the specific of each milestone? What muste we ensure happen in the simulation before each milestone?",
  StopConditionXIdea: "What is the stop condition for the simulation?",
  StopConditionXGrounding:
    "What are the specific of the stop conditions? What muste we ensure happen in the simulation before the stop condition?",
  FailureConditionXIdea: "What are the failure conditions for the simulation?",
  FailureConditionXGrounding:
    "What are the specifics of each failure conditions? Why does this indicate that the simulation has gone wrong?",
};

const SetMatrix = () => {
  const { currentPrototype, updateIsLoading, updatePrototypes } =
    useAppContext();
  const [problem, setProblem] = useState("");
  const [expand, setExpand] = useState(true);

  const [AgentsXIdea, setAgentsXIdea] = useState("");
  const [ActionsXIdea, setActionsXIdea] = useState("");
  const [LocationsXIdea, setLocationsXIdea] = useState("");
  const [MilestonesXIdea, setMilestonesXIdea] = useState("");
  const [StopConditionXIdea, setStopConditionXIdea] = useState("");
  const [FailureConditionXIdea, setFailureConditionXIdea] = useState("");
  const [AgentsXGrounding, setAgentsXGrounding] = useState("");
  const [ActionsXGrounding, setActionsXGrounding] = useState("");
  const [LocationsXGrounding, setLocationsXGrounding] = useState("");
  const [MilestonesXGrounding, setMilestonesXGrounding] = useState("");
  const [StopConditionXGrounding, setStopConditionXGrounding] = useState("");
  const [failureConditionXGrounding, setFailureConditionXGrounding] =
    useState("");

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
    const fetchInput = async () => {
      updateIsLoading(true);
      try {
        const agentsXIdea = await getInput("AgentsXIdea");
        setAgentsXIdea(agentsXIdea);
        const actionsXIdea = await getInput("ActionsXIdea");
        setActionsXIdea(actionsXIdea);
        const locationsXIdea = await getInput("LocationsXIdea");
        setLocationsXIdea(locationsXIdea);
        const milestonesXIdea = await getInput("MilestonesXIdea");
        setMilestonesXIdea(milestonesXIdea);
        const stopConditionXIdea = await getInput("StopConditionXIdea");
        setStopConditionXIdea(stopConditionXIdea);
        const failureConditionXIdea = await getInput("FailureConditionXIdea");
        setFailureConditionXIdea(failureConditionXIdea);
        const agentsXGrounding = await getInput("AgentsXGrounding");
        setAgentsXGrounding(agentsXGrounding);
        const actionsXGrounding = await getInput("ActionsXGrounding");
        setActionsXGrounding(actionsXGrounding);
        const locationsXGrounding = await getInput("LocationsXGrounding");
        setLocationsXGrounding(locationsXGrounding);
        const milestonesXGrounding = await getInput("MilestonesXGrounding");
        setMilestonesXGrounding(milestonesXGrounding);
        const stopConditionXGrounding = await getInput(
          "StopConditionXGrounding",
        );
        setStopConditionXGrounding(stopConditionXGrounding);
        const failureConditionXGrounding = await getInput(
          "FailureConditionXGrounding",
        );
        setFailureConditionXGrounding(failureConditionXGrounding);
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
                    width: "21%",
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
                    width: "21%",
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
                    width: "21%",
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
                    LOCATIONS
                  </Typography>
                </TableCell>
                <TableCell
                  sx={{
                    width: "21%",
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
                    MILESTONES
                  </Typography>
                </TableCell>
                <TableCell
                  sx={{
                    width: "21%",
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
                    STOPCONDITION
                  </Typography>
                </TableCell>
                <TableCell
                  sx={{
                    width: "21%",
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
                    FAILURECONDITION
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["LocationsXIdea"]}
                  </Typography>
                  <Typography variant="body2">{LocationsXIdea}</Typography>
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["MilestonesXIdea"]}
                  </Typography>
                  <Typography variant="body2">{MilestonesXIdea}</Typography>
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["StopConditionXIdea"]}
                  </Typography>
                  <Typography variant="body2">{StopConditionXIdea}</Typography>
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["FailureConditionXIdea"]}
                  </Typography>
                  <Typography variant="body2">
                    {FailureConditionXIdea}
                  </Typography>
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["LocationsXGrounding"]}
                  </Typography>
                  <Typography variant="body2">{LocationsXGrounding}</Typography>
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["MilestonesXGrounding"]}
                  </Typography>
                  <Typography variant="body2">
                    {MilestonesXGrounding}
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["StopConditionXGrounding"]}
                  </Typography>
                  <Typography variant="body2">
                    {StopConditionXGrounding}
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
                    {MATRIX_CATEGORY_DESCRIPTIONS["FailureConditionXGrounding"]}
                  </Typography>
                  <Typography variant="body2">
                    {failureConditionXGrounding}
                  </Typography>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </>
    </Stack>
  );
};

export default SetMatrix;
