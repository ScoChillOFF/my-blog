import React, { useState } from "react";
import TextInput from "./TextInput.jsx";
import TextArea from "./TextArea.jsx";
import Button from "../../../generic/Button.jsx";
import styles from "./CreateArticleForm.module.css";

const CreateArticleForm = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState("");
  const [show, setShow] = useState(false);
  const isReadyToSubmit = title.length != 0 && content.length != 0;

  function onCreateSubmit(event) {
    event.preventDefault();
    const article = {
      title: title,
      content: content,
      tags: tags.length == 0 ? [] : tags.split(" "),
    };
    setTitle("");
    setContent("");
    setTags("");
    console.log(article);
  }

  if (!show) {
    return (
      <form className={styles.createForm + " " + styles.notShow} action="">
        <div className={styles.headerContainer}>
          <h3>Create article</h3>
          <span onClick={() => setShow(true)}>+</span>
        </div>
      </form>
    );
  }

  return (
    <form className={styles.createForm} action="">
      <div className={styles.headerContainer}>
        <h3>Create article</h3>
        <span onClick={() => setShow(false)}>-</span>
      </div>
      <TextInput
        jsonField="title"
        placeholder="Article title"
        onChange={setTitle}
        value={title}
      />
      <TextArea
        jsonField="content"
        placeholder="Article content"
        value={content}
        onChange={setContent}
      />
      <TextInput
        jsonField="tags"
        placeholder="Tags separated by whitespace"
        onChange={setTags}
        value={tags}
      />
      <div>
        <div></div>
        <Button
          onClick={onCreateSubmit}
          text="Create article"
          disabled={!isReadyToSubmit}
        />
      </div>
    </form>
  );
};

export default CreateArticleForm;
