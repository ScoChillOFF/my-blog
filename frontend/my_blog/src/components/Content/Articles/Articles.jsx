import React from 'react'
import styles from './Articles.module.css'
import CreateArticleForm from './CreateArticle/CreateArticleForm.jsx'

const Articles = () => {
  return (
    <div className={styles.articles}>
      <CreateArticleForm />
    </div>
  )
}

export default Articles