PORT 8000
GET /canvas -> (returns all the canvas names)
POST /canvas -> (returns canvas_id)
GET /canvas/{canvas_id} -> (returns details of all the images in the canvas)
POST /canvas/{canvas_id}/{image_id} -> (add new image in the canvas, returns true/false)
PUT /canvas/{canvas_id} -> (refresh/update canvas data)
DELETE /canvas/{canvas_id}/{image_id} -> (remove selected image, returns true/false)
