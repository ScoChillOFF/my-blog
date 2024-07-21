import React, { useState } from "react";
import axios from "axios";
import RadioInput from "../../generic/RadioInput";
import CheckboxInput from "../../generic/CheckboxInput";
import Button from "../../generic/Button";
import styles from "./FilterSection.module.css";

const FilterSection = ({ onApply, tags }) => {
  const [daysLimit, setDaysLimit] = useState(null);
  const [selectedTagNames, setSelectedTagNames] = useState([]);

  async function getFilteredArticles() {
    console.log("Applied filters");
    let url = "http://127.0.0.1:8000/api/v1/articles?";
    if (daysLimit != null) {
      url += "days_limit=" + daysLimit;
    }
    if (selectedTagNames != []) {
      for (let tagName of selectedTagNames) {
        url += "&tags=" + tagName
      }
    }
    const response = await axios.get(url);
    return response.data;
  }

  async function applyFilters() {
    const filteredArticles = await getFilteredArticles();
    onApply(filteredArticles, selectedTagNames);
  }

  function onTagSelect(targetTagName) {
    const newSelectedTagNames = [...selectedTagNames, targetTagName];
    setSelectedTagNames(newSelectedTagNames);
  };

  function onTagUnselect(targetTagName) {
    const newSelectedTagNames = selectedTagNames.filter((tagName) => tagName != targetTagName);
    setSelectedTagNames(newSelectedTagNames);
  };

  return (
    <div className={styles.filterSection}>
      <form className={styles.daysFilter}>
        <h3>By date</h3>
        <RadioInput
          label={"All time"}
          name={"days-filter"}
          value={null}
          selectedValue={daysLimit}
          onChange={() => setDaysLimit(null)}
        />
        <RadioInput
          label={"Last day"}
          name={"days-filter"}
          value={1}
          selectedValue={daysLimit}
          onChange={() => setDaysLimit(1)}
        />
        <RadioInput
          label={"Last 3 days"}
          name={"days-filter"}
          value={3}
          selectedValue={daysLimit}
          onChange={() => setDaysLimit(3)}
        />
        <RadioInput
          label={"Last 7 days"}
          name={"days-filter"}
          value={3}
          selectedValue={daysLimit}
          onChange={() => setDaysLimit(7)}
        />
        <RadioInput
          label={"Last 30 days"}
          name={"days-filter"}
          value={30}
          selectedValue={daysLimit}
          onChange={() => setDaysLimit(30)}
        />
      </form>
      <form className={styles.tagsFilter}>
        <h3>By tags</h3>
        {tags.map((tag) => (
          <CheckboxInput
            label={tag.name}
            name="tags-filter"
            value={tag.name}
            key={tag.id}
            onSelect={onTagSelect}
            onUnselect={onTagUnselect}
          />
        ))}
      </form>
      <Button text="Apply" onClick={applyFilters} />
    </div>
  );
};

export default FilterSection;
