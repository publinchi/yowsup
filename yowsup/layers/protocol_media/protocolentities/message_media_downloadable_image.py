from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
class ImageDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}" 
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <media type="{{DOWNLOADABLE_MEDIA_TYPE: (image | audio | video)}}"
            mimetype="{{MIME_TYPE}}" 
            filehash="{{FILE_HASH}}"
            url="{{DOWNLOAD_URL}}" 
            ip="{{IP}}"
            size="{{MEDIA SIZE}}"
            file="{{FILENAME}}" 


            encoding="{{ENCODING}}" 
            height="{{IMAGE_HEIGHT}}" 
            width="{{IMAGE_WIDTH}}"
            
            > {{THUMBNAIL_RAWDATA (JPEG?)}}
        </media>
    </message>
    '''
    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName,
            encoding, width, height, caption = None, preview = None, 
            _id = None, _from = None, to = None, notify = None, timestamp = None, 
            participant = None, offline = None, retry = None):

        super(ImageDownloadableMediaMessageProtocolEntity, self).__init__("image",
            mimeType, fileHash, url, ip, size, fileName,
            _id, _from, to, notify, timestamp, participant, offline, retry)
        self.setImageProps(encoding, width, height, caption, preview)

    def __str__(self):
        out  = super(ImageDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Encoding: %s\n" % self.encoding
        out += "Width: %s\n" % self.width
        out += "Height: %s\n" % self.height
        if self.caption:
            out += "Caption: %s\n" % self.caption
        return out

    def setImageProps(self, encoding, width, height, caption, preview):
        self.encoding   = encoding
        self.width      = int(width)
        self.height     = int(height)
        self.caption    = caption
        self.preview    = preview

    def getCaption(self):
        return self.caption
        
    def getPreview(self):
        return self.preview

    def toProtocolTreeNode(self):
        node = super(ImageDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("encoding",  self.encoding)
        mediaNode.setAttribute("width",     str(self.width))
        mediaNode.setAttribute("height",    str(self.height))
        if self.caption:
            mediaNode.setAttribute("caption", self.caption)
        mediaNode.setData(self.preview)
        
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ImageDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setImageProps(
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("width"),
            mediaNode.getAttributeValue("height"),
            mediaNode.getAttributeValue("caption"),
            mediaNode.getData()
        )
        return entity
