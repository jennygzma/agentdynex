import React, { ReactElement, ReactNode } from "react";
import { Box as MuiBox, BoxProps as MuiBoxProps } from "@mui/material";

interface BoxProps extends MuiBoxProps {
  children?: ReactNode;
  border?: number;
}

const Box = ({ children, border, sx, ...props }: BoxProps): ReactElement => {
  return (
    <MuiBox
      sx={{
        padding: "10px",
        border: border ?? 10,
        borderColor: "#9d5ba3ff",
        backgroundColor: "white",
        ...sx,
      }}
      {...props}
    >
      {children}
    </MuiBox>
  );
};

export default Box;
