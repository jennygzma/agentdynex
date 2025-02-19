import { useState } from "react";
import Box from "../../../components/Box";
import { useAppContext } from "../hooks/app-context";
import { Drawer, Stack, styled, Tooltip, Typography } from "@mui/material";
import React from "react";
import Button from "../../../components/Button";
import Prototypes from "./prototypes";
import { ChevronLeft, Menu } from "@mui/icons-material";

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

const Header = () => {
  const [sidebarIsOpen, setSidebarIsOpen] = useState(false);
  const { prototypes, updateCurrentPrototype } = useAppContext();

  const toggleDrawer = (toggleValue) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }
    setSidebarIsOpen(toggleValue);
  };

  return (
    <Box
      sx={{
        backgroundColor: "#9d5ba3ff",
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        width: "100%", // Ensure the header spans the full width
        zIndex: 1300, // Ensure it stays above other content (MUI default zIndex for drawers)
        padding: "10px",
      }}
    >
      <Stack
        direction="row"
        spacing="10px"
        sx={{
          alignItems: "center",
          justifyContent: "space-between",
          width: "98%",
          paddingRight: "10px",
        }}
      >
        <Button
          onClick={toggleDrawer(!sidebarIsOpen)}
          colorVariant={"transparent"}
        >
          <Menu />
        </Button>
        <Drawer
          anchor="left"
          open={sidebarIsOpen}
          onClose={toggleDrawer(false)}
        >
          <DrawerHeader
            sx={{
              paddingTop: "100px",
            }}
          >
            <Button onClick={toggleDrawer(false)}>
              <ChevronLeft />
            </Button>
          </DrawerHeader>
          <Prototypes />
        </Drawer>
        <Stack
          direction="row"
          sx={{
            alignItems: "center",
          }}
        >
          <img
            src={require("../../../assets/robin.ico")}
            alt="franky"
            width="50x"
          />
          <Typography
            variant="h4"
            sx={{
              // alignSelf: "center",
              color: "white",
              fontWeight: "bold",
              fontFamily: "Courier New",
              textAlign: "center",
            }}
          >
            AGENTDYNEX
          </Typography>
        </Stack>
        {prototypes?.length !== 0 ? (
          <Tooltip title="Explore a new prototype!">
            <Button
              onClick={() => {
                updateCurrentPrototype(undefined);
              }}
              sx={{ ml: "auto", alignSelf: "right" }}
            >
              +
            </Button>
          </Tooltip>
        ) : (
          <Box sx={{ backgroundColor: "#9d5ba3ff" }}> </Box>
        )}
      </Stack>
    </Box>
  );
};

export default Header;
