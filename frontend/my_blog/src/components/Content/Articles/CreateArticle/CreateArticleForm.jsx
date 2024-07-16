import React from "react";
import TextInput from "./TextInput.jsx";
import TextArea from "./TextArea.jsx";
import Button from "../../../generic/Button.jsx";
import styles from "./CreateArticleForm.module.css";

const CreateArticleForm = () => {
  function onCreateSubmit(event) {
    event.preventDefault();
    console.log(1);
  }

  return (
    <form className={styles.createForm} action="">
      <h3>Create article</h3>
      <TextInput jsonField="title" placeholder="Article title" />
      <TextArea jsonField="content" placeholder="Article content" />
      <TextInput jsonField="tags" placeholder="Tags, separated by whitespace" />
      <div>
        <div></div>
        <Button onClick={onCreateSubmit} text="Create article" />
      </div>
    </form>
  );
};

export default CreateArticleForm;
