import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Divider,
  Flex,
  GridItem,
} from "@chakra-ui/react"
import {
  canExpand,
  descriptionId,
  FormContextType,
  getTemplate,
  getUiOptions,
  ObjectFieldTemplateProps,
  RJSFSchema,
  StrictRJSFSchema,
  titleId,
} from "@rjsf/utils"
import { Location } from "@components/map/Map"
import MapPopover from "@components/map/MapPopover"

export default function ObjectFieldTemplate<
  T = any,
  S extends StrictRJSFSchema = RJSFSchema,
  F extends FormContextType = any
>(props: ObjectFieldTemplateProps<T, S, F>) {
  const {
    description,
    title,
    properties,
    required,
    disabled,
    readonly,
    uiSchema,
    idSchema,
    schema,
    formData,
    onAddClick,
    registry,
  } = props
  const uiOptions = getUiOptions<T, S, F>(uiSchema)
  const TitleFieldTemplate = getTemplate<"TitleFieldTemplate", T, S, F>("TitleFieldTemplate", registry, uiOptions)
  const DescriptionFieldTemplate = getTemplate<"DescriptionFieldTemplate", T, S, F>(
    "DescriptionFieldTemplate",
    registry,
    uiOptions
  )
  // Button templates are not overridden in the uiSchema
  const {
    ButtonTemplates: { AddButton },
  } = registry.templates

  const map = "map" in uiOptions && uiOptions["map"] ? uiOptions["map"] : false
  const mapTitle = "mapTitle" in uiOptions && uiOptions["mapTitle"] ? uiOptions["mapTitle"].toString() : "Location"

  return title ? (
    <AccordionItem borderStyle={"none"} width={"100%"}>
      <AccordionButton display={"flex"} justifyContent={"space-between"}>
        {title && (
          <TitleFieldTemplate
            id={titleId<T>(idSchema)}
            title={title}
            required={required}
            schema={schema}
            uiSchema={uiSchema}
            registry={registry}
          />
        )}
        {description && (
          <DescriptionFieldTemplate
            id={descriptionId<T>(idSchema)}
            description={description}
            schema={schema}
            uiSchema={uiSchema}
            registry={registry}
          />
        )}
        <AccordionIcon fontSize={24} />
      </AccordionButton>
      <Divider />

      <AccordionPanel display={"flex"} flexWrap={"wrap"} width={"100%"} justifyContent={"space-between"} gap={5}>
        {properties.map((element, index) =>
          element.hidden ? (
            element.content
          ) : (
            <GridItem minWidth={"35%"} key={`${idSchema.$id}-${element.name}-${index}`}>
              {element.content}
            </GridItem>
          )
        )}
        {map && (
          <GridItem justifySelf="flex-end">
            <Flex
              justifyContent={"space-around"}
              flexDirection={"column"}
              paddingTop={"25px"}
              width={"100%"}
              height={"100%"}
            >
              <MapPopover
                key={`${
                  (props.formContext &&
                    props.formContext.getLastManualUpdate &&
                    props.formContext.getLastManualUpdate()) ||
                  "blank"
                }`}
                focusMarker={{ title: mapTitle, location: { ...formData } as Location }}
                locationChange={(location) =>
                  props.formContext && props.formContext.setLocation && props.formContext.setLocation(location)
                }
              />
            </Flex>
          </GridItem>
        )}
        {canExpand<T, S, F>(schema, uiSchema, formData) && (
          <GridItem justifySelf="flex-end">
            <AddButton
              className="object-property-expand"
              onClick={onAddClick(schema)}
              disabled={disabled || readonly}
              uiSchema={uiSchema}
              registry={registry}
            />
          </GridItem>
        )}
      </AccordionPanel>
    </AccordionItem>
  ) : (
    <Flex display={"flex"} flexWrap={"wrap"} width={"100%"} justifyContent={"space-between"} gap={5}>
      {properties.map((element, index) =>
        element.hidden ? (
          element.content
        ) : (
          <GridItem minWidth={"45%"} key={`${idSchema.$id}-${element.name}-${index}`}>
            {element.content}
          </GridItem>
        )
      )}
    </Flex>
  )
}
