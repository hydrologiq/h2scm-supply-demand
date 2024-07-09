import { useEffect, useState } from "react"
import { Box, Grid, GridItem, Tag } from "@chakra-ui/react"
import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api"
import { roundToDP } from "@utils/math"
import "./Map.css"

const containerStyle = {
  width: "100%",
  height: "100%",
}

export type LocationMarker = {
  location: Location
  title: string
  privateMode?: string
}

export interface Location {
  lat: number
  long: number
}

export interface LatLong {
  lat: number
  lng: number
}

export interface MapProps {
  focusMarker?: LocationMarker
  locationChange?: (location: Location) => void
  zoom?: number
  markers?: LocationMarker[]
}

const center: Location = {
  lat: 54.97101,
  long: -2.45682,
}

const Map = ({ focusMarker, locationChange, zoom = 8, markers = [] }: MapProps) => {
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: import.meta.env.VITE_G_MAPS_API_KEY,
  })

  const [loc, setLoc] = useState<Location>((focusMarker && focusMarker.location) || center)

  useEffect(() => {
    locationChange && locationChange(loc)
  }, [loc])

  if (focusMarker && focusMarker.location) markers = [focusMarker, ...markers]

  return (
    <>
      <Box height={"400px"} width={"400px"} pb={5}>
        {markers.length > 0 && (
          <Grid templateColumns={`repeat(2, 1fr)`}>
            {markers.map((marker, index) => (
              <GridItem key={`${marker.location.lat}-${marker.location.long}-${index}`}>
                <Tag background={"none"} className={marker.privateMode ? marker.privateMode : ""}>
                  {index + 1} - {marker.title}
                </Tag>
              </GridItem>
            ))}
          </Grid>
        )}
        {isLoaded && (
          <GoogleMap
            mapContainerStyle={containerStyle}
            center={{ lat: loc.lat, lng: loc.long }}
            zoom={zoom}
            options={{ streetViewControl: false, mapTypeControl: false, fullscreenControl: false }}
            onClick={(ev: google.maps.MapMouseEvent) => {
              if (ev.latLng) {
                setLoc({ lat: roundToDP(ev.latLng.lat(), 5), long: roundToDP(ev.latLng.lng(), 5) })
              }
            }}
          >
            {markers.map((marker, index) => (
              <Marker
                position={{ lat: marker.location.lat, lng: marker.location.long }}
                title={marker.title}
                label={{ text: `${index + 1}` }}
                key={`${marker.location.lat}-${marker.location.long}-${index}`}
              />
            ))}
          </GoogleMap>
        )}
      </Box>
    </>
  )
}

export default Map
