import { Checkbox, FormControlLabel, Stack, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import Box from "../../../../components/Box";
import TextField from "../../../../components/TextField";
import Button from "../../../../components/Button";
import InputWithButton from "../../../../components/InputWithButton";
import { useAppContext } from "../../hooks/app-context";
import { CategoryType, useMatrixContext } from "../../hooks/matrix-context";
import Chip from "../../../../components/Chip";
import { SERVER_URL } from "../..";

interface CategoryProps {
  category: CategoryType;
  description: string;
  isDependency: boolean;
}

const Category = ({
  description,
  category,
  isDependency = false,
}: CategoryProps) => {
  const { updateIsLoading, currentPrototype } = useAppContext();
  const {
    submittedProblem,
    updateUpdatedMatrix,
    currentCategory,
    updateCurrentCategory,
    updateMatrixCategoryInfo,
    matrixCategoryInfo,
  } = useMatrixContext();
  let initialInput = "";
  let initialActionsInput = [];
  let initialBrainstorm = [];

  // use input for all but ActionsXIdea
  const [input, setInput] = useState(initialInput);
  const isCheckbox = category.includes("Idea");
  const [actionsInput, setActionsInput] = useState(initialActionsInput);

  const [brainstorms, setBrainstorms] = useState(initialBrainstorm);
  const [newActionsBrainstorm, setNewActionsBrainstorm] = useState("");

  const [iteration, setIteration] = useState("");
  const isGrounding = category.includes("Grounding");
  const ideaPair = category.split("X")[0] + "XIdea";
  const disabled = isGrounding && matrixCategoryInfo[ideaPair].length === 0;
  const [isCheckboxChanged, setIsCheckboxChanged] = useState(false);
  const [versions, setVersions] = useState([]);

  const getInput = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/get_input`,
      params: {
        category: category,
      },
    })
      .then((response) => {
        console.log("/get_input request successful:", response.data);
        setInput(response.data.input);
      })
      .catch((error) => {
        console.error("Error calling /get_input request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const updateInput = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: `${SERVER_URL}/update_input`,
      data: {
        category: category,
        input: isCheckbox ? actionsInput : input,
      },
    })
      .then((response) => {
        console.log("/update_input request successful:", response.data);
        getInput();
      })
      .catch((error) => {
        console.error("Error calling /update_input request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const brainstormInputs = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: `${SERVER_URL}/brainstorm_inputs`,
      params: {
        category: category,
        iteration: iteration,
        brainstorms: brainstorms,
      },
    })
      .then((response) => {
        console.log("/brainstorm_inputs request successful:", response.data);
        if (isGrounding) {
          setInput(response.data.brainstorms);
        } else {
          setBrainstorms([...brainstorms, ...response.data.brainstorms]);
        }
      })
      .catch((error) => {
        console.error("Error calling /brainstorm_inputs request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {}, [submittedProblem]);

  useEffect(() => {}, [currentPrototype]);

  const handleCheckBoxChange =
    (name: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      if (event.target.checked) {
        setActionsInput([...actionsInput, name]);
      } else {
        setActionsInput(actionsInput.filter((value) => value !== name));
      }
      setIsCheckboxChanged(true);
    };

  return (
    <Box
      border={0}
      sx={{
        maxWidth: "700px",
        width: "400px",
        borderColor: isDependency ? "#F8F3CA" : "transparent",
        backgroundColor: isDependency ? "#F8F3CA" : "transparent",
      }}
    >
      <Stack spacing="10px">
        <Typography
          variant="body2"
          sx={{
            fontWeight: "bold",
          }}
        >
          {description}
        </Typography>
        <Button
          onClick={() => {
            brainstormInputs();
            if (currentCategory !== category) {
              updateCurrentCategory(category);
            }
          }}
          disabled={disabled}
          sx={{
            width: "100%",
          }}
        >
          Brainstorm
        </Button>
        {brainstorms?.length > 0 || input ? (
          <Stack direction="row" spacing="5px">
            <TextField
              label="Iterate"
              className={"Iterate"}
              rows={1}
              value={iteration}
              onChange={(e) => {
                setIteration(e.target.value);
              }}
            />
            <Button
              onClick={brainstormInputs}
              disabled={disabled}
              sx={{
                width: "20%",
              }}
            >
              Update
            </Button>
          </Stack>
        ) : (
          <></>
        )}
        {isCheckbox ? (
          <div>
            <Stack direction="column">
              {brainstorms?.map((brainstorm) => (
                <FormControlLabel
                  key={brainstorm}
                  control={
                    <Checkbox
                      checked={actionsInput.includes(brainstorm)}
                      onChange={handleCheckBoxChange(brainstorm)}
                      sx={{
                        color: "purple",
                        "&.Mui-checked": {
                          color: "purple",
                        },
                      }}
                    />
                  }
                  label={brainstorm}
                />
              ))}
            </Stack>
            <InputWithButton
              label="Input"
              input={newActionsBrainstorm}
              setInput={setNewActionsBrainstorm}
              onClick={() => {
                setBrainstorms([...brainstorms, newActionsBrainstorm]);
                setNewActionsBrainstorm("");
              }}
              onChange={() => {
                if (currentCategory !== category) {
                  updateCurrentCategory(category);
                }
              }}
              direction="row"
              buttonName="+"
              rows={category.includes("Idea") ? 1 : 8}
            />
          </div>
        ) : (
          brainstorms?.map((brainstorm) => {
            return (
              <Chip
                key={brainstorm}
                label={brainstorm}
                onClick={() => {
                  setInput(brainstorm);
                  if (currentCategory !== category) {
                    updateCurrentCategory(category);
                  }
                }}
                clickable
                selected={brainstorm === input}
                sx={{
                  alignSelf: "center",
                }}
              />
            );
          })
        )}
        {isCheckbox ? (
          <Button
            onClick={() => {
              updateInput();
              updateUpdatedMatrix(true);
              updateMatrixCategoryInfo(category, actionsInput);
              if (currentCategory !== category) {
                updateCurrentCategory(category);
              }
              setIsCheckboxChanged(false);
            }}
            disabled={disabled || !isCheckboxChanged}
          >
            Submit
          </Button>
        ) : (
          <InputWithButton
            label="Input"
            input={input}
            setInput={setInput}
            disabled={disabled}
            onClick={() => {
              updateInput();
              updateUpdatedMatrix(true);
              updateMatrixCategoryInfo(category, input);
              if (currentCategory !== category) {
                updateCurrentCategory(category);
              }
            }}
            onChange={() => {
              if (currentCategory !== category) {
                updateCurrentCategory(category);
              }
            }}
            direction="column"
            rows={category.includes("Idea") ? 1 : 8}
          />
        )}
        {isGrounding && (
          <Stack spacing="5px">
            <Button
              disabled={disabled}
              onClick={() => {
                setVersions([...versions, input]);
                if (currentCategory !== category) {
                  updateCurrentCategory(category);
                }
              }}
            >
              Save Version
            </Button>
            {versions?.map((version) => (
              <Chip
                key={version}
                label={version}
                onClick={() => {
                  setInput(version);
                }}
                clickable
                selected={version === input}
                sx={{
                  alignSelf: "center",
                  maxWidth: "698px",
                }}
              />
            ))}
          </Stack>
        )}
      </Stack>
    </Box>
  );
};

export default Category;
