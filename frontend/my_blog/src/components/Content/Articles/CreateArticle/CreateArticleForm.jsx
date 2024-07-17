import React, { useState } from "react";
import axios from "axios"
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

  async function sendArticleToServerAndUpdate(article) {
    const response = await axios.post("http://127.0.0.1:8000/api/v1/articles", article);
    return response.data;
  }

  async function onCreateSubmit(event) {
    event.preventDefault();
    let article = {
      title: title,
      content: content,
      tags: tags.length == 0 ? [] : tags.split(" "),
    };
    article = await sendArticleToServerAndUpdate(article);
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
