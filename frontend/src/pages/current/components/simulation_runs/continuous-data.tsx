import React, { useState } from "react";
import { Stack, Typography, Divider } from "@mui/material";
import ChangeLog from "./change-log";
import Dynamics from "./dynamics-table";
import Button from "../../../../components/Button";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import HumanHijack from "./human-hijack";

const ContinuousData = ({ parentExpand }: { parentExpand: boolean }) => {
  const [expand, setExpand] = useState(parentExpand);

  if (!expand) {
    return (
      <Stack spacing="20px">
        <HumanHijack />
        <Divider />
        <Stack direction="row" spacing="10px" sx={{ alignItems: "center" }}>
          <Button onClick={() => setExpand(true)}>
            <ExpandMore fontSize="small" />
          </Button>
          <Typography variant="h6" sx={{ fontWeight: "bold" }}>
            INTERMEDIATE SUMMARIES
          </Typography>
        </Stack>
        <Divider />
      </Stack>
    );
  }
  return (
    <Stack spacing="20px">
      <HumanHijack />
      <Divider />
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
          INTERMEDIATE SUMMARIES
        </Typography>
      </Stack>
      <Stack
        direction="row"
        spacing="20px"
        sx={{ justifyContent: "space-between" }}
      ></Stack>
      <Stack direction="row" spacing="10px">
        <Stack width="66%" spacing="10px">
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            Change Summary
          </Typography>
          <ChangeLog expand={expand} />
        </Stack>
        <Stack width="34%" spacing="10px">
          <Typography
            variant="h6"
            sx={{
              fontWeight: "bold",
            }}
          >
            Dynamics Summary
          </Typography>
          <Dynamics expand={expand} />
        </Stack>
      </Stack>
      <Divider />
    </Stack>
  );
};

export default ContinuousData;
