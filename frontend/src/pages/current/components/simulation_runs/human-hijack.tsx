import React, { useEffect, useRef, useState, useCallback } from "react";
import {
  Stack,
  Typography,
  Divider,
  Grid,
  Checkbox,
  Radio,
  Box,
} from "@mui/material";
import axios from "axios";
import { SERVER_URL } from "../..";
import { useAppContext } from "../../hooks/app-context";
import ChangeLog from "./change-log";
import Dynamics from "./dynamics-table";
import TextField from "../../../../components/TextField";
import Button from "../../../../components/Button";
import { CheckBox, ExpandLess, ExpandMore } from "@mui/icons-material";
import InputWithButton from "../../../../components/InputWithButton";

type AgentLocation = {
  agent: string;
  location: string;
};
type AgentStatement = {
  agent: string;
  statement: string;
};
type LocationAgents = {
  location: string;
  agents: Array<string>;
};

const HumanHijack = () => {
  const DEMO = false;

  const [agents, setAgents] = useState([
    "Luffy",
    "Sanji",
    "Zoro",
    "Nami",
    "Usopp",
    "Robin",
    "Franky",
    "Chopper",
    "Brook",
    "Jinbei",
  ]);
  const [locations, setLocations] = useState(["Sunny", "Alabasta", "Wano"]);
  const [locationAgents, setLocationAgents] = useState<LocationAgents[]>([
    {
      location: "Thousand Sunny",
      agents: ["Usopp", "Nami", "Chopper", "Brook"],
    },
    { location: "Wano", agents: ["Robin", "Franky", "Jinbei"] },
    { location: "Alabasta", agents: ["Luffy", "Zoro", "Sanji"] },
  ]);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<string | null>(null);
  const [move, setMove] = useState<AgentLocation | undefined>(undefined);

  const [agentSpeaking, setAgentSpeaking] = useState<string | null>(null);
  const [statement, setStatement] = useState<string>("");
  const [submitted, setSubmitted] = useState<{
    agent: string;
    statement: string;
  } | null>(null);

  const dynamicReflectionProblem = "Luffy wants to eat meat";
  const dynamicReflectionSolution =
    "1. Sanji moves to ship \n2. Sanji cooks Luffy meat";

  const [expand, setExpand] = useState(true);

  const [dynamicReflection, setDynamicReflection] = useState("");

  const { isRunningSimulation, currentPrototype, currentRunId } =
    useAppContext();

  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Use useCallback to create a stable function reference for getDynamicReflection
  const getDynamicReflection = () => {
    // Add a try/catch to handle any errors gracefully
    try {
      axios({
        method: "GET",
        url: `${SERVER_URL}/get_dynamic_reflection`,
      })
        .then((response) => {
          console.log(
            "/get_dynamic_reflection request successful:",
            response.data,
          );
          setDynamicReflection(response.data.dynamic_reflection);
        })
        .catch((error) => {
          console.error(
            "Error calling /get_dynamic_reflection request:",
            error,
          );
        });
    } catch (error) {
      console.error("Exception in getDynamicReflection:", error);
    }
  };

  useEffect(() => {
    console.log(
      "useEffect: isRunningSimulation changed to",
      isRunningSimulation,
    );

    // Always clear any existing interval first
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    // Set a new interval if simulation is running
    if (isRunningSimulation) {
      // Get the reflection once immediately
      getDynamicReflection();

      // Then set the interval for future updates - use direct function reference
      intervalRef.current = setInterval(getDynamicReflection, 60002);
    }

    // Cleanup on unmount or state change
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isRunningSimulation]); // Remove getDynamicReflection from dependencies

  const handleSubmitMove = () => {
    if (selectedAgent && selectedLocation) {
      setMove({ agent: selectedAgent, location: selectedLocation });
    }
    setSelectedAgent(null);
    setSelectedLocation(null);
  };

  const handleSubmitStatement = () => {
    if (agentSpeaking && statement?.trim()) {
      setSubmitted({ agent: agentSpeaking, statement });
      setStatement("");
    }
    setAgentSpeaking(null);
    setStatement("");
  };

  if (!expand) {
    return (
      <Stack direction="row" spacing="20px" sx={{ alignItems: "center" }}>
        <Button onClick={() => setExpand(true)}>
          <ExpandMore fontSize="small" />
        </Button>
        <Typography variant="h6" sx={{ fontWeight: "bold" }}>
          NUDGING
        </Typography>
      </Stack>
    );
  }

  return (
    <Stack spacing="20px">
      <Stack direction="row" spacing="10px" sx={{ alignItems: "center" }}>
        <Button onClick={() => setExpand(false)} sx={{ width: "30px" }}>
          <ExpandLess fontSize="small" />
        </Button>
        <Typography
          variant="h6"
          sx={{
            fontWeight: "bold",
          }}
        >
          NUDGING
        </Typography>
      </Stack>
      <Stack spacing="20px" direction="row">
        <Stack width="25%" spacing="20px">
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            Dynamic Reflection
          </Typography>

          {DEMO ? (
            <Stack spacing="10px">
              <Stack direction="row" spacing="10px" width="100%">
                <Stack spacing="10px" width="50%">
                  <Typography
                    variant="body1"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    PROBLEM
                  </Typography>
                  <TextField
                    className={"problem"}
                    rows={8}
                    value={dynamicReflectionProblem}
                    readOnly={true}
                    code={true}
                  />
                </Stack>
                <Stack spacing="10px" width="50%">
                  <Typography
                    variant="body1"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    SOLUTION
                  </Typography>
                  <TextField
                    className={"solution"}
                    rows={8}
                    value={dynamicReflectionSolution}
                    readOnly={true}
                    code={true}
                  />
                </Stack>
              </Stack>
              <Stack
                spacing="10px"
                direction="row"
                sx={{ alignItems: "center", justifyContent: "space-between" }}
              >
                <Typography
                  variant="body1"
                  sx={{
                    fontWeight: "bold",
                  }}
                >
                  APPLY?
                </Typography>

                <Stack spacing="10px" alignItems="center" direction="row">
                  <Button>YES</Button>
                  <Button>NO</Button>
                </Stack>
              </Stack>
            </Stack>
          ) : (
            <TextField
              className={"reflect"}
              rows={13}
              value={dynamicReflection}
              readOnly={true}
              code={true}
            />
          )}
        </Stack>

        <Divider orientation="vertical" />
        <Stack spacing="20px">
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            Manual Intervention
          </Typography>
          <Stack direction="row" spacing="10px">
            <Stack spacing="10px">
              <Typography
                variant="body1"
                sx={{
                  fontWeight: "bold",
                }}
              >
                CURRENT LOCATIONS:
              </Typography>
              <Stack direction="row" spacing="10px">
                {locationAgents?.map((locationAgents, index) => {
                  return (
                    <Stack spacing="5px" key={index}>
                      <Typography variant="body2">
                        📍 {locationAgents.location}
                      </Typography>
                      <TextField
                        className={locationAgents.location}
                        rows={10}
                        value={locationAgents?.agents
                          ?.map((agent) => `👤 ${agent}`)
                          .join("\n")}
                        readOnly={true}
                        code={true}
                      ></TextField>
                    </Stack>
                  );
                })}
              </Stack>
            </Stack>
            <Divider orientation="vertical" />
            <Stack spacing="10px">
              <Typography
                variant="body1"
                sx={{
                  fontWeight: "bold",
                }}
              >
                MOVE
              </Typography>
              <Typography fontWeight="bold">👤 Agents:</Typography>
              <Grid container>
                {agents.map((agent) => (
                  <Grid item xs={3} key={agent}>
                    <Stack direction="row" alignItems="center">
                      <Checkbox
                        checked={selectedAgent === agent}
                        onChange={() => setSelectedAgent(agent)}
                        sx={{
                          color: "purple",
                          "&.Mui-checked": {
                            color: "purple",
                          },
                        }}
                      />
                      <Typography>{agent}</Typography>
                    </Stack>
                  </Grid>
                ))}
              </Grid>

              <Typography fontWeight="bold">📍 Locations:</Typography>
              <Grid container>
                {locations.map((location) => (
                  <Grid item xs={3} key={location}>
                    <Stack direction="row" alignItems="center">
                      <Checkbox
                        checked={selectedLocation === location}
                        onChange={() => setSelectedLocation(location)}
                        sx={{
                          color: "purple",
                          "&.Mui-checked": {
                            color: "purple",
                          },
                        }}
                      />
                      <Typography>{location}</Typography>
                    </Stack>
                  </Grid>
                ))}
              </Grid>

              <Button
                variant="contained"
                onClick={handleSubmitMove}
                disabled={!selectedAgent || !selectedLocation}
              >
                Submit Move
              </Button>

              {move && (
                <Typography>
                  ✅ Move submitted: {move.agent} → {move.location}
                </Typography>
              )}
            </Stack>
            <Divider orientation="vertical" />
            <Stack spacing="10px">
              <Typography
                variant="body1"
                sx={{
                  fontWeight: "bold",
                }}
              >
                AGENT SAYS
              </Typography>
              <Typography fontWeight="bold">👤 Agents:</Typography>
              <Grid container>
                {agents.map((agent) => (
                  <Grid item xs={2} key={agent}>
                    <Stack direction="row" alignItems="center">
                      <Radio
                        checked={agentSpeaking === agent}
                        onChange={() => setAgentSpeaking(agent)}
                        value={agent}
                        sx={{
                          color: "purple",
                          "&.Mui-checked": {
                            color: "purple",
                          },
                        }}
                      />
                      <Typography>{agent}</Typography>
                    </Stack>
                  </Grid>
                ))}
              </Grid>

              {agentSpeaking && (
                <TextField
                  placeholder={`What should ${agentSpeaking} say?`}
                  value={statement}
                  onChange={(e) => setStatement(e.target.value)}
                />
              )}

              <Button
                variant="contained"
                onClick={handleSubmitStatement}
                disabled={!agentSpeaking || !statement.trim()}
              >
                Submit Statement
              </Button>

              {submitted && (
                <Typography>
                  ✅ {submitted.agent} said: "{submitted.statement}"
                </Typography>
              )}
            </Stack>
          </Stack>
        </Stack>
      </Stack>
    </Stack>
  );
};

export default HumanHijack;
