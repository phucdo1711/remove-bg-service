import React, { Fragment, useEffect, useState, useCallback } from "react";
import { Button, Card, Col, Row, Typography, Upload } from "antd";
import {
  LoadingOutlined,
  PlusOutlined,
  InboxOutlined,
  DownloadOutlined,
  SwapOutlined,
} from "@ant-design/icons";
import styles from "./StyleTransferPage.module.scss";
import axios from "utils/axios";
import { useDropzone } from "react-dropzone";
import ImagePicker from "components/ImagePicker";
import candyImg from "assets/style-images/candy.jpg";
import mosaicImg from "assets/style-images/mosaic.jpg";
import starryNightImg from "assets/style-images/starry-night.jpg";
import udnieImg from "assets/style-images/udnie.jpg";

const { Title } = Typography;

function getBase64(img, callback) {
  const reader = new FileReader();
  reader.addEventListener("load", () => callback(reader.result));
  reader.readAsDataURL(img);
}

const images = [
  {
    src: candyImg,
    id: "candy",
  },
  {
    src: mosaicImg,
    id: "mosaic",
  },
  {
    src: starryNightImg,
    id: "starry-night",
  },
  {
    src: udnieImg,
    id: "udnie",
  },
];

const StyleTransferPage = () => {
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [file, setFile] = useState(null);
  const [styleId, setStyleId] = useState(images[0].id);
  const [result, setResult] = useState(null);
  const onDrop = useCallback((acceptedFiles) => {
    // Do something with the files
    const file = acceptedFiles[0];
    if (!file) return;
    setResult(null);
    getBase64(file, setImageUrl);
    setFile(file);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
    accept: "image/*",
    maxFiles: 1,
  });

  const uploadButton = (
    <div>
      <Fragment>
        <p className="ant-upload-drag-icon" style={{ marginBottom: 24 }}>
          <InboxOutlined style={{ fontSize: 64, color: "#1890ff" }} />
        </p>
        <p className="ant-upload-text">
          Click or drag file to this area to upload
        </p>
        <p className="ant-upload-hint">
          Support for a single or bulk upload. Strictly prohibit from uploading
          company data or other band files
        </p>
      </Fragment>
    </div>
  );

  const onTranfer = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post("/api/style-transfer", formData, {
        headers: {
          "content-type": "multipart/form-data",
        },
        params: {
          model: styleId,
        },
        responseType: "arraybuffer",
      });
      setResult("data:image/png;base64," + Buffer.from(res.data, "binary").toString("base64"));
    } catch (error) {
      alert(error.message);
    }
    setLoading(false);
  };

  return (
    <Row>
      <Col sm={24} md={10} className={styles.col}>
        <Title level={5}>Choose an image style:</Title>
        <ImagePicker images={images} value={styleId} onChange={setStyleId} />
        <Title level={5}>Select your image:</Title>
        <div className={styles.uploadWrapper}>
          <div {...getRootProps()} className={styles.avatarUploader}>
            <input {...getInputProps()} />
            {imageUrl ? (
              <img
                src={imageUrl}
                alt="avatar"
                style={{ maxWidth: "100%", maxHeight: "100%" }}
              />
            ) : (
              uploadButton
            )}
          </div>
        </div>
      </Col>
      <Col
        sm={24}
        md={4}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Button
          icon={<SwapOutlined />}
          size="large"
          type="primary"
          style={{ maxWidth: "100%" }}
          disabled={!file}
          loading={loading}
          onClick={onTranfer}
        >
          Transfer Image
        </Button>
      </Col>
      <Col sm={24} md={10} className={styles.col}>
        {result && (
          <ResultImage
            imageUrl={result}
            title={`Tranfered image (${styleId})`}
          />
        )}
      </Col>
    </Row>
  );
};

const ResultImage = ({ imageUrl, title }) => {
  const download = () => {
    window.location.href = imageUrl;
    var a = document.createElement("a"); //Create <a>
    a.href = imageUrl; //Image Base64 Goes here
    a.download = `image-result.png`; //File name Here
    a.click();
  };

  return (
    <Card
      title={title}
      extra={
        imageUrl && (
          <Button
            type="primary"
            shape="round"
            icon={<DownloadOutlined />}
            onClick={download}
          />
        )
      }
      style={{ marginBottom: 16 }}
    >
      <img src={imageUrl} style={{ maxWidth: "100%" }} />
    </Card>
  );
};

export default StyleTransferPage;
