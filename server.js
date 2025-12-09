import express from 'express'
import mongoose from 'mongoose'
import cors from 'cors'
import dotenv from 'dotenv'
import authRoutes from './routes/auth.js'
import chatRoutes from './routes/chat.js'
import stripeRoutes from './routes/stripe.js'

dotenv.config()

const app = express()
app.use(cors())
app.use(express.json())

app.use('/api/auth', authRoutes)
app.use('/api/chat', chatRoutes)
app.use('/api/stripe', stripeRoutes)

const PORT = process.env.PORT || 4000

mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(()=>{
    app.listen(PORT, ()=> console.log(`Server on ${PORT}`))
  }).catch(err=> console.error('Mongo error', err))
