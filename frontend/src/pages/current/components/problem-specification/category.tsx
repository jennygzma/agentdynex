import { Badge, Stack, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import axios from "axios";
import Box from "../../../../components/Box";
import TextField from "../../../../components/TextField";
import Button from "../../../../components/Button";
import InputWithButton from "../../../../components/InputWithButton";
import { useAppContext } from "../../hooks/app-context";
import { CategoryType } from "../../hooks/matrix-context";
import Chip from "../../../../components/Chip";

interface CategoryProps {
  category: CategoryType;
  description: string;
}

interface Specification {
  question: string;
  brainstorm: string[];
  answer: string;
}

const mapQuestionsToSpecifications = (
  questions: Array<string>,
): Array<Specification> =>
  questions.map((question) => ({
    question: question,
    brainstorm: [],
    answer: "",
  }));

const Category = ({ description, category }: CategoryProps) => {
  const { updateIsLoading } = useAppContext();
  const [input, setInput] = useState("");
  const [needsSpecification, setNeedsSpecification] = useState(false);
  const [specifications, setSpecifications] = useState([]);

  const updateSpecificationBrainstorm = (
    index: number,
    brainstorm: string[],
  ) => {
    const updatedSpecifications = specifications.map((spec, i) =>
      i === index ? { ...spec, brainstorm: brainstorm } : spec,
    );
    setSpecifications(updatedSpecifications);
  };

  const updateSpecificationAnswer = (index: number, answer: string) => {
    const updatedSpecifications = specifications.map((spec, i) =>
      i === index ? { ...spec, answer: answer } : spec,
    );
    setSpecifications(updatedSpecifications);
  };

  const getNeedsSpecification = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: "/get_needs_specification",
      data: {
        category: category,
      },
    })
      .then((response) => {
        console.log(
          "/get_needs_specification request successful:",
          response.data,
        );
        setNeedsSpecification(response.data.needs_specification);
      })
      .catch((error) => {
        console.error("Error calling /get_needs_specification request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getInput = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: "/get_input",
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
      url: "/update_input",
      data: {
        category: category,
        input: input,
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

  const getQuestions = () => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: "/get_questions",
      params: {
        category: category,
      },
    })
      .then((response) => {
        console.log("/get_questions request successful:", response.data);
        setSpecifications(
          mapQuestionsToSpecifications(response.data.questions),
        );
      })
      .catch((error) => {
        console.error("Error calling /get_questions request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const getBrainstorm = (question: string, index: number) => {
    updateIsLoading(true);
    axios({
      method: "GET",
      url: "/get_questions",
      params: {
        category: category,
        question: question,
      },
    })
      .then((response) => {
        console.log("/get_questions request successful:", response.data);
        updateSpecificationBrainstorm(index, response.data.brainstorm);
      })
      .catch((error) => {
        console.error("Error calling /get_questions request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  const updateSpecifications = () => {
    updateIsLoading(true);
    axios({
      method: "POST",
      url: "/update_specifications",
      data: {
        category: category,
        specifications: specifications,
      },
    })
      .then((response) => {
        console.log(
          "/update_specifications request successful:",
          response.data,
        );
        getInput();
        getNeedsSpecification();
      })
      .catch((error) => {
        console.error("Error calling /update_specifications request:", error);
      })
      .finally(() => {
        updateIsLoading(false);
      });
  };

  useEffect(() => {
    getInput();
    getNeedsSpecification();
  }, []);

  return (
    <Box border={5} sx={{ padding: "10px" }}>
      <Stack spacing="10px">
        {needsSpecification && (
          <Badge
            badgeContent={"Needs Specification"}
            anchorOrigin={{ vertical: "top", horizontal: "right" }}
            color="primary"
            sx={{
              top: 8,
              right: 70,
              "& .MuiBadge-badge": {
                backgroundColor: "lightblue",
                color: "white",
                fontWeight: "bold",
                fontFamily: "monospace",
              },
            }}
          />
        )}
        <Typography
          variant="subtitle1"
          sx={{
            fontWeight: "bold",
            alignSelf: "center",
            fontFamily: "monospace",
          }}
        >
          {category}
        </Typography>
        <Typography
          variant="body2"
          sx={{
            alignSelf: "center",
            fontFamily: "monospace",
          }}
        >
          {description}
        </Typography>
        <InputWithButton
          label="Input"
          input={input}
          setInput={setInput}
          onClick={updateInput}
          direction="column"
        />
        <Button
          onClick={getQuestions}
          disabled={!needsSpecification}
          sx={{
            width: "100%",
          }}
        >
          Specify
        </Button>
        {specifications.map(({ question, brainstorms, answer }, index) => {
          return (
            <Stack key={index} spacing="5px">
              <Stack direction="row" spacing="5px">
                <Typography
                  variant="body1"
                  sx={{
                    fontWeight: "bold",
                    fontFamily: "monospace",
                  }}
                >
                  {question}
                </Typography>{" "}
                <Button onClick={() => getBrainstorm(question, index)}>
                  💡
                </Button>
              </Stack>
              {brainstorms.map((brainstorm) => {
                <Chip
                  key={brainstorm}
                  label={brainstorm}
                  onClick={() => {
                    updateSpecificationAnswer(index, brainstorm);
                  }}
                  clickable
                  selected={brainstorm === answer}
                />;
              })}
              <TextField
                className={`${index}-answer`}
                label="Answer"
                value={answer}
                rows={1}
                onChange={(e) => {
                  updateSpecificationAnswer(index, e.target.value);
                }}
              ></TextField>
            </Stack>
          );
        })}
        <Button
          onClick={updateSpecifications}
          disabled={!needsSpecification}
          sx={{
            width: "100%",
          }}
        >
          Update Specifications
        </Button>
      </Stack>
    </Box>
  );
};

export default Category;
