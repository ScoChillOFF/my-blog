import React, { useState } from "react";
import styles from "./CheckboxInput.module.css"

const CheckboxInput = ({ label, name, value, onSelect, onUnselect }) => {
  const [isChecked, setIsChecked] = useState(false);

  function handleChange() {
    if (!isChecked) {
      onSelect(value);
    } else {
      onUnselect(value);
    }
    setIsChecked(!isChecked);
  };

  return (
    <label className={styles.checkbox}>
      <input
        type="checkbox"
        name={name}
        value={value}
        checked={isChecked}
        onChange={handleChange}
        />
      {label}
    </label>
  );
};

export default CheckboxInput;
