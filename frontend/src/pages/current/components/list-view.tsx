import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import axios from "axios";
import { useAppContext } from "../hooks/app-context";
import { SERVER_URL } from "..";

type ListItem = {
  problem: string;
  problem_example: string;
  solution: string;
  solution_example: string;
};

interface ListProps {
    type: "iterative" | "static"
 }

const List = ({type}: ListProps) => {
  const [listData, setListData] = useState<ListItem[]>([]);
  const { updateIsLoading } = useAppContext();
  console.log(listData);
  useEffect(() => {
    console.log("hi jenny");
    if (type === "iterative") {
        getIterativeList();
    } else {
        getStaticList();
    }
  }, []);

  const getStaticList = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_static_list`,
    })
      .then((response) => {
        console.log("/get_static_list request successful:", response.data);
        setListData(response.data.list);
      })
      .catch((error) => {
        console.error("Error calling /get_static_list request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getIterativeList = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_iterative_list`,
    })
      .then((response) => {
        console.log("/get_iterative_list request successful:", response.data);
        setListData(response.data.list);
      })
      .catch((error) => {
        console.error("Error calling /get_iterative_list request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Problem</TableCell>
            <TableCell>Problem Example</TableCell>
            <TableCell>Solution</TableCell>
            <TableCell>Solution Example</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {listData.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.problem}</TableCell>
              <TableCell>{row.problem_example}</TableCell>
              <TableCell>{row.solution}</TableCell>
              <TableCell>{row.solution_example}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default List;
