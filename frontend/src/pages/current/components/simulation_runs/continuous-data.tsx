import React, { useEffect, useState } from "react";
import { Stack, Typography, Divider } from "@mui/material";
import axios from "axios";
import { SERVER_URL } from "../..";
import { useAppContext } from "../../hooks/app-context";
import ChangeLog from "./change-log";
import Dynamics from "./dynamics-table";
import TextField from "../../../../components/TextField";
import Button from "../../../../components/Button";
import { ExpandLess, ExpandMore } from "@mui/icons-material";

const ContinuousData = ({ parentExpand }: { parentExpand: boolean }) => {
  const [expand, setExpand] = useState(parentExpand);

  const [status, setStatus] = useState("");

  const { isRunningSimulation } = useAppContext();
  const getStatus = () => {
    // updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_status`,
    })
      .then((response) => {
        console.log("/get_status request successful:", response.data);
        setStatus(response.data.status);
      })
      .catch((error) => {
        console.error("Error calling /get_status request:", error);
      })
      .finally(() => {
        // updateIsLoading(false);
      });
  };

  useEffect(() => {
    if (isRunningSimulation && expand) {
      const intervalId = setInterval(getStatus, 30000);
      return () => clearInterval(intervalId);
    } else {
      setStatus("");
    }
  }, [isRunningSimulation]);

  if (!expand) {
    return (
      <Stack direction="row" spacing="10px" sx={{ alignItems: "center" }}>
        <Button onClick={() => setExpand(true)}>
          <ExpandMore fontSize="small" />
        </Button>
        <Typography variant="body1" sx={{ fontWeight: "bold" }}>
          SIMULATION DATA
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
          variant="body1"
          sx={{
            fontWeight: "bold",
          }}
        >
          SIMULATION DATA
        </Typography>
      </Stack>
      <Stack direction="row" sx={{ justifyContent: "space-between" }}>
        <Typography
          variant="h6"
          sx={{
            fontWeight: "bold",
          }}
        >
          Status
        </Typography>
      </Stack>
      <TextField
        className={"Status"}
        rows={3}
        value={status}
        readOnly={true}
        code={true}
      />
      <Divider />
      <Stack direction="row" spacing="10px">
        <Stack width="66%">
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            Change Log
          </Typography>
          <ChangeLog expand={expand} />
        </Stack>
        <Stack width="34%">
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            Notable Dynamics
          </Typography>
          <Dynamics expand={expand} />
        </Stack>
      </Stack>

      <Divider />
    </Stack>
  );
};

export default ContinuousData;
