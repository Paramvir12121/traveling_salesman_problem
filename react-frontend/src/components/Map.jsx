import React from 'react'
import {useLoadScript} from "@react-google-maps/api"

function Map() {
    const {isLoaded } = useLoadScript({
        googleMapsApiKey: process.env.NEXT_PUBLIC_JAVASCRIPT_API
    })

  return (
    <>
    <div>Map</div>
    <div>{process.env.NEXT_PUBLIC_JAVASCRIPT_API}</div>
    </>
  )
}

export default Map